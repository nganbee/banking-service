import pandas as pd
import re
import math
from difflib import get_close_matches
from app.clients.ollama_client import ollama_client
from app.core.settings import settings
from app.core.schemas import AgentState, IntentResult

class IntentClassification:
    def __init__(self):

        self.client = ollama_client
        self.model_name = settings.FINETUNED_MODEL
        self.mapping_path = "app/data/intent_mapping.csv"
        
        print(f"--- CONNECTING TO OLLAMA VIA PINGGY ---")    
        
        # Vẫn cần load mapping để thực hiện hậu xử lý (Normalize/Map label)
        self.class_list_str = self._get_class_intent(self.mapping_path)
        self.known_labels = self.class_list_str.split("\n")
        self.norm_map = {self._normalize_intent_label(l): l for l in self.known_labels}

    def _get_class_intent(self, mapping_path):
        try:
            df_label = pd.read_csv(mapping_path)
            return "\n".join(df_label['name_intent'].tolist())
        except Exception as e:
            print(f"Error load file mapping: {e}")
            return ""
        
    def _normalize_intent_label(self, text):
        cleaned_text = str(text).strip().lower()
        cleaned_text = re.sub(r"[^a-z0-9]+", "_", cleaned_text)
        cleaned_text = re.sub(r"_+", "_", cleaned_text).strip("_")
        return cleaned_text

    def _map_to_known_label(self, prediction):
        normalized_prediction = self._normalize_intent_label(prediction)
        if normalized_prediction in self.norm_map:
            return self.norm_map[normalized_prediction]
        
        for normalized_label, original_label in self.norm_map.items():
            if normalized_label in normalized_prediction or normalized_prediction in normalized_label:
                return original_label

        close_matches = get_close_matches(normalized_prediction, list(self.norm_map.keys()), n=1, cutoff=0.8)
        return self.norm_map[close_matches[0]] if close_matches else "unknown"
    
    def _get_prompt(self, text):

        return f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Classify the intent of the following banking customer query.
Rule: Output ONLY the exact intent name in these label.
{self.class_list_str}

### Input:
{text}

### Response:
"""

    def predict(self, message):
        try:
            result = self.client.generate(
                model=self.model_name,
                prompt=self._get_prompt(message),
                return_full=True
            )
            
            raw_text = result["text"]
            intent_from_text = self._map_to_known_label(raw_text)
            logprobs_list = result.get("logprobs", [])
            
            relevant_logprobs = [item['logprob'] for item in logprobs_list if item['token'] in intent_from_text]
    
            if relevant_logprobs:
                # Lấy toàn bộ logprobs của các token sinh ra
                # (Tránh việc lọc token bị sót do sub-words hoặc space)
                avg_lp = sum(relevant_logprobs) / len(relevant_logprobs)
                confidence = round(math.exp(avg_lp), 2)
            else:
                confidence = 0.6 if intent_from_text != "unknown" else 0.0
            
            return intent_from_text, confidence
        except Exception as e:
            print(f"Error in predict via OllamaClient: {e}")
            return "unknown", 0.0

classifier = IntentClassification()

def intent_node(state: AgentState) -> AgentState:
    print(f"\n--- [NODE] Intent Detection ---")
    predicted_intent, cofi = classifier.predict(state.customer_message)
    
    state.intent_data = IntentResult(intent=predicted_intent, confidence=cofi)
    state.trace.append(f"Intent: {predicted_intent}")
    print(f"Result: {predicted_intent}")
    print(f"Cofidence: {cofi}")
    return state
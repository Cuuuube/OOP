
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class anekdot_gen:
    DEVICE = torch.device("cuda:0")
    model_name_or_path = "./GTPpretrained"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path, bos_token='<s>', eos_token='</s>')
    model = GPT2LMHeadModel.from_pretrained(model_name_or_path).to(DEVICE)
    anek_ed = "А где"
    def __init__(self, text):
        self.anek_st = text

    def text_tokenization(self, text):
        text = '<s> ' + text + '</s>'
        input_ids = self.tokenizer.encode(text, return_tensors="pt").to(self.DEVICE)
        return input_ids
    
    def generation(self):
        #Вероятностное сэмплирование с ограничением
        input_ids = self.text_tokenization(self.anek_st)
        self.model.eval()
        with torch.no_grad():
            out = self.model.generate(input_ids, 
                                do_sample=True,
                                num_beams=2,
                                temperature=1.5,
                                top_p=0.9,
                                max_length=70,
                                )

        generated_text = list(map(self.tokenizer.decode, out))[0]
        anek_without_tr = ""
        for i in range(0, len(generated_text) - 1):
            if ((generated_text[i] == "[") and (generated_text[i+1] == "E") and
                (generated_text[i+2] == "J") and (generated_text[i+3] == "]")):
                break 
            elif ((generated_text[i] == "[") or (generated_text[i] == "S") or
                (generated_text[i] == "J") or (generated_text[i] == "]") or 
                (generated_text[i] == "<") or (generated_text[i] == ">") or 
                (generated_text[i] == "s") or (generated_text[i] == "/")):
                i+=1
            elif generated_text[i] == "-" and generated_text[i+1] == " ":
                anek_without_tr += "\n-"
            else:
                anek_without_tr += generated_text[i] 
        print(anek_without_tr)
        self.anek_ed = anek_without_tr

    def anek_print(self):
        print(self.anek_ed)
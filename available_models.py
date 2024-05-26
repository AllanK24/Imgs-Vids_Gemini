import google.generativeai as genai

def print_models():
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(model.name)
            
if __name__=="__main__":
    print_models()

from services.MicrolinkClient import *
from services.MyLLM import MyTemplater, MyLLM

m = MyLLM("You are a helpful assistant")
t = MyTemplater("./templates")

prompt = t.generate(
    "prompt_refiner.md",
    prompt="We are 118118Money. We offer loans from £1k to £5k from 12 months to 5 years with representative APR of 49.9%. Write an engaging marketing email to encourage the customers to log in to their account to get a chance to enter into a prize draw.",
)

prompt2 = m.generate(prompt, keep_history=False)
m.generate(prompt2)
m.print_last_message()

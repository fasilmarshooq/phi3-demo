"""
Main chat application with Phi-3 model and function calling support.
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import time
from .function_handler import parse_function_call, execute_function_call, get_system_context

def generate_response(model, tokenizer, prompt, max_tokens=150):
    """Generate response from the model"""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=max_tokens,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )
    
    # Extract generated response
    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]
    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    
    return {
        'text': generated_text,
        'input_tokens': inputs["input_ids"].shape[1],
        'output_tokens': len(generated_tokens)
    }

def handle_function_calls(model, tokenizer, user_input, generated_text, system_context):
    """Handle function calls and generate final response"""
    function_calls = parse_function_call(generated_text)
    
    if not function_calls:
        return generated_text, [], 0, 0
    
    print("🔧 Executing function calls...")
    
    # Execute function calls and collect results
    function_results = []
    for call in function_calls:
        result = execute_function_call(call['function'], call['argument'])
        function_results.append(f"{call['function']}: {result}")
        print(f"✅ {call['function']}({call['argument'] or ''}) executed")
    
    # Generate final response with function results
    final_prompt = f"""{system_context}
<|user|>
{user_input}<|end|>
<|assistant|>
{generated_text}

Function Results:
{chr(10).join(function_results)}

Based on this information:"""
    
    # Generate final response
    final_response = generate_response(model, tokenizer, final_prompt, max_tokens=100)
    
    return final_response['text'], function_calls, final_response['input_tokens'], final_response['output_tokens']

def chat():
    """Main chat loop"""
    print("🤖 Loading Phi-3 model...")
    
    model_name = "microsoft/phi-3-mini-4k-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    print("\nWelcome to the Phi-3 mini chatbot with function calling!")
    print("Type 'quit' or 'exit' to end the conversation.")
    print("💡 Try asking about Agoda policies, bookings, or deals!")
    print("-" * 60)
    
    system_context = get_system_context()
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! Thanks for chatting!")
            break
            
        if not user_input:
            print("Please enter a message or type 'quit' to exit.")
            continue
        
        # Start timing
        start_time = time.time()
        
        # Initial prompt for function calling decision
        prompt = f"""{system_context}
<|user|>
{user_input}<|end|>
<|assistant|>"""

        print("Phi-3 is thinking...")
        
        # Generate initial response
        initial_response = generate_response(model, tokenizer, prompt)
        generated_text = initial_response['text']
        input_token_count = initial_response['input_tokens']
        
        # Handle function calls if present
        final_response, function_calls, final_input_tokens, final_output_tokens = handle_function_calls(
            model, tokenizer, user_input, generated_text, system_context
        )
        
        # Display response
        if function_calls:
            print(f"Phi-3🔧: {final_response}")
            # Update token counts for function calling
            output_token_count = initial_response['output_tokens'] + final_output_tokens
            total_tokens = input_token_count + final_input_tokens + final_output_tokens
        else:
            # No function calls, just display the response
            response = generated_text.replace("<|end|>", "").strip()
            print(f"Phi-3: {response}")
            output_token_count = initial_response['output_tokens']
            total_tokens = input_token_count + output_token_count
        
        # End timing and display metrics
        end_time = time.time()
        response_time = end_time - start_time
        
        func_info = f" + {len(function_calls)} func" if function_calls else ""
        print("-" * 60)
        print(f"📊 {response_time:.2f}s | {input_token_count}→{output_token_count} tokens ({total_tokens} total) | {output_token_count/response_time:.1f} tok/s{func_info}")

if __name__ == "__main__":
    chat()
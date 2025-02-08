import openai
from dotenv import load_dotenv
import os
from prompt import data_code_generator

load_dotenv()

class StandardizeFormatCodeGenerator:
    def __init__(self, input_row):
        self.client = openai.OpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=os.getenv("TOGETHER_API_KEY")
        )
        self.model="deepseek-ai/DeepSeek-V3"
    
    def generate(self):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": data_code_generator.code_gen_system_prompt},
                {"role": "user", "content": """
                 1. **crypto_payments_table**:
                    - Columns: `log_id`, `transaction_id`, `gateway_name`, `gateway_transaction_id`, `gateway_status`, `gateway_amount`, `gateway_currency`, `gateway_response`, `timestamp`
                    - Example Row: `3e2ec2f4-83b5-4f1c-af81-7ea0dfe710f6, Payment Gateway X, 4fac1400-2ee8-488b-9fdd-04ff52959024, Success, 4836.35, USD, Success, 26/12/2024 16:42`

                    2. **e_wallet_transactions_table**:
                    - Columns: `transaction_id`, `user_account`, `payment_method`, `transaction_value`, `transaction_status`, `transaction_category`, `transaction_time`
                    - Example Row: `00b47933-36b3-4725-82e0-0308348670a2, USR87263, Touch 'n Go, 3295.13, Unsuccessful, Top-up, 07/02/2025 8:12`

                    3. **fpx_transactions_table**:
                    - Columns: `transaction_id`, `account_id`, `bank`, `amount`, `status`, `transaction_type`, `timestamp`
                    - Example Row: `017f4cf2-7664-4921-96e3-6c2f091e87b1, ACC12345, Maybank, 2251.05, Successful, Deposit, 28/12/2024 15:51`
                 """}
            ],
            temperature=0.0
        )

        return (response.choices[0].message.content)
    
    
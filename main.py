from code_generator import StandardizeFormatCodeGenerator
from db_connection.db_utils import upload_to_mysql

if __name__ == '__main__':
    code_gen = StandardizeFormatCodeGenerator('')
    generated_code = code_gen.generate()
    clean_code = generated_code.replace("```python", "", 1).strip("```")
    upload_to_mysql(clean_code, 'payment')
    
    
from code_generator import StandardizeFormatCodeGenerator
import tqdm

if __name__ == '__main__':
    code_gen = StandardizeFormatCodeGenerator('')
    generated_code = code_gen.generate()
    print(generated_code)
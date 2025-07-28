import os

def get_words_from_file(file_path: str) -> set:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = set(line.strip() for line in file if line.strip())
        return words
    except Exception as e:
        print(f"Error reading file: {e}")
        return set()

def add_word_to_file(word: str, file_path: str):
    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"\n{word}")
        print(f"'{word}' added to the file.")
    except Exception as e:
        print(f"Error adding word to file: {e}")
        
# def add_word_to_file(word):
#    try:
#         words = get_words_from_file(file_path)
#         if word not in words:
#             words.add(word)
#             sorted_words = sorted(words)

#             temp_path = "tmp_" + file_path
#             with open(temp_path, "w", encoding="utf-8") as temp_file:
#                 temp_file.write("\n".join(sorted_words))
#             os.replace(temp_path, file_path)
#             print(f"'{word}' added to the file.")
#         else:
#             print(f"'{word}' already exists in the file.")
#    except Exception as e:
#        print(f"Error adding word to file: {e}")

def order_words_in_file(file_path: str):
    try:
        words = get_words_from_file(file_path)
        sorted_words = sorted(words)
        
        temp_path = "tmp_" + file_path
        with open(temp_path, "w", encoding="utf-8") as temp_file:
            temp_file.write("\n".join(sorted_words))
        os.replace(temp_path, file_path)
        print("Words in file ordered successfully.")
    except Exception as e:
        print(f"Error ordering words in file: {e}")
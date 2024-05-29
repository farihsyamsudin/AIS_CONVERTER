import csv

def char_to_decimal(char):
    char_info = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, ':': 10, ';': 11, '<': 12, '=': 13, '>': 14, '?': 15,
        '@': 16, 'A': 17, 'B': 18, 'C': 19, 'D': 20, 'E': 21, 'F': 22, 'G': 23,
        'H': 24, 'I': 25, 'J': 26, 'K': 27, 'L': 28, 'M': 29, 'N': 30, 'O': 31,
        'P': 32, 'Q': 33, 'R': 34, 'S': 35, 'T': 36, 'U': 37, 'V': 38, 'W': 39,
        "'": 40, 'a': 41, 'b': 42, 'c': 43, 'd': 44, 'e': 45, 'f': 46, 'g': 47,
        'h': 48, 'i': 49, 'j': 50, 'k': 51, 'l': 52, 'm': 53, 'n': 54, 'o': 55,
        'p': 56, 'q': 57, 'r': 58, 's': 59, 't': 60, 'u': 61, 'v': 62, 'w': 63
    }
    return char_info.get(char, None)

def ascii_to_decimal(ascii_value):
    return ord(ascii_value)

def decimal_to_bits(decimal_value):
    return bin(decimal_value)[2:].zfill(6)

def binary_to_decimal(binary_data):
    decimal_value = int(binary_data, 2)
    return decimal_value

def binary_to_signed_decimal(binary_data):
    decimal_value = int(binary_data, 2)
    if binary_data[0] == "1":  # Check if the first bit is 1 (negative value)
        decimal_value -= 2 ** len(binary_data)
    return decimal_value

def binary_to_decimal_fraction(binary_data, denominator):
    decimal_value = binary_to_signed_decimal(binary_data)
    return decimal_value / denominator

def parse_ais_data(binary_data):
    parsed_data = {
        "Message Type": binary_to_decimal(binary_data[0:6]),
        "Repeat Indicator": binary_to_decimal(binary_data[6:8]),
        "MMSI": binary_to_decimal(binary_data[8:38]),
        "Navigation Status": binary_to_decimal(binary_data[38:42]),
        "Rate of Turn (ROT)": binary_to_decimal(binary_data[42:50]),
        "Speed Over Ground": binary_to_decimal(binary_data[50:60]),
        "Position Accuracy": binary_to_decimal(binary_data[60:61]),
        "Longitude": binary_to_decimal_fraction(binary_data[61:89], 600000),
        "Latitude": binary_to_decimal_fraction(binary_data[89:116], 600000),
        "Course Over Ground": binary_to_decimal_fraction(binary_data[116:128], 10),
        "True Heading": binary_to_decimal(binary_data[128:137]),
        "Time Stamp": binary_to_decimal(binary_data[137:143]),
        "Manuver Indicator": binary_to_decimal(binary_data[143:145]),
        "Spare": binary_to_decimal(binary_data[145:148]),
        "RAIM Flag": binary_to_decimal(binary_data[148:149]),
        "Radio Status": binary_to_decimal(binary_data[149:168])
    }
    return parsed_data

def extract_data_from_csv(file_path):
    extracted_data = []

    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row and row[0].startswith('!AIVDM'):
                if len(row) >= 6:
                    data = row[5]  # Mengambil bit ke-6 dari setiap baris
                    if len(data) == 28:  # Hanya ambil data dengan format yang diinginkan
                        extracted_data.append(data)
                    

    return extracted_data

def print_parsed_data(data_mentah, parsed_data, output_file):
    print("From Data:", data_mentah, file=output_file)
    print("Message Type:", parsed_data["Message Type"], file=output_file)
    print("Repeat Indicator:", parsed_data["Repeat Indicator"], file=output_file)
    print("MMSI:", parsed_data["MMSI"], file=output_file)
    print("Navigation Status:", parsed_data["Navigation Status"], file=output_file)
    print("Rate of Turn (ROT):", parsed_data["Rate of Turn (ROT)"], file=output_file)
    print("Speed Over Ground:", parsed_data["Speed Over Ground"], file=output_file)
    print("Position Accuracy:", parsed_data["Position Accuracy"], file=output_file)
    print("Longitude:", parsed_data["Longitude"], file=output_file)
    print("Latitude:", parsed_data["Latitude"], file=output_file)
    print("Course Over Ground:", parsed_data["Course Over Ground"], file=output_file)
    print("True Heading:", parsed_data["True Heading"], file=output_file)
    print("Time Stamp:", parsed_data["Time Stamp"], file=output_file)
    print("Manuver Indicator:", parsed_data["Manuver Indicator"], file=output_file)
    print("Spare:", parsed_data["Spare"], file=output_file)
    print("RAIM Flag:", parsed_data["RAIM Flag"], file=output_file)
    print("Radio Status:", parsed_data["Radio Status"], file=output_file)

def process_row(data, output_file):
    data_mentah = data
    if len(data) == 28 and data.count("`") <= 3:
        binary_data = ""
        for char in data:
            # Kayanya Salah disini
            # Proses -> Char To ASCII, ASCII To Decimal dengan biner 6 bit
            ascii_value = ascii_to_decimal(char)
            decimal_value = char_to_decimal(char)
            if decimal_value is not None:
                binary_data += decimal_to_bits(decimal_value)

        parsed_data = parse_ais_data(binary_data)
        print_parsed_data(data_mentah, parsed_data, output_file)
        print("===", file=output_file)  # Separator antara setiap data


def remove_quotes(input_path, output_path):
    with open(input_path, 'r') as input_file, open(output_path, 'w', newline='') as output_file:
        content = input_file.read()
        cleaned_content = content.replace('"', '')  # Menghapus karakter kutip ganda
        output_file.write(cleaned_content)


def main():
    input_csv_path = 'Example_Data/data.csv'
    output_csv_path = 'Example_Data/process_file.csv'
    remove_quotes(input_csv_path, output_csv_path)

    extracted_data = extract_data_from_csv(output_csv_path)
    # for data in extracted_data:
    #     print("Data:", data)
    #     process_row(data)

    with open('result.txt', 'w') as output_file:
        for data in extracted_data:
            process_row(data, output_file)

if __name__ == "__main__":
    main()

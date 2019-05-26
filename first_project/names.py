from name_function import  get_formatted_name

print("Enter 'q' at any time to quit.")
while True:
    first = input("\nPlease give me your first name:")
    if first == 'q':
        break
    last = input("\nPlease give me your last name:")
    if last == 'q':
        break

    formatted_name = get_formatted_name(first, last)
    print("\tNeatly fotnatted name:" + formatted_name + '.')
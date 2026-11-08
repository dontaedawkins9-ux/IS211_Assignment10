
import sqlite3

def query_pets():
    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()

    while True:
        user_input = input("Enter a person's ID (-1 to exit): ")

        try:
            person_id = int(user_input)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if person_id == -1:
            print("Goodbye!")
            break

        cursor.execute(
            "SELECT * FROM person WHERE id = ?",
            (person_id,)
        )

        person = cursor.fetchone()

        if person is None:
            print("Error: Person not found.")
            continue

        print(f"\n{person[1]} {person[2]}, {person[3]} years old")

        cursor.execute("""
            SELECT pet.name, pet.breed, pet.age, pet.dead
            FROM pet
            JOIN person_pet ON pet.id = person_pet.pet_id
            WHERE person_pet.person_id = ?
        """, (person_id,))

        pets = cursor.fetchall()

        if not pets:
            print("This person has no pets.")

        for pet in pets:
            name, breed, age, dead = pet

            status = "deceased" if dead == 1 else "alive"

            print(
                f"{person[1]} {person[2]} owned "
                f"{name}, a {breed}, "
                f"that was {age} years old ({status})."
            )

        print()

    conn.close()


if __name__ == "__main__":
    query_pets()

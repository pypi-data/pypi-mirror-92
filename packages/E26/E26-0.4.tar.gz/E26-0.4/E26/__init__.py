from random import randint as r
import base64

class E26Error(Exception):
    pass


class E26StringDoesNotMatchError(E26Error):
    msg = """String doesn't match. Try again!"""
    pass


class E26SyntaxError(E26Error, SyntaxError):
    msg = """Please do not use UPPERCASE Charaters or Special characters"""
    pass


class E26Hash:
    r"""

        ## How it works:
        E26 is a new string encoding method. It works with 2 necessary strings:
        - The string who need to be encoded
        - The secret Token (generated randomly)

        ## To encode the string we need the token.
        This encoding are using a big matrix with all characters.
        Every letter of the word need to have an X position, to get the Y postion we need the token.
        With these 2 positions now we can encode our string, finding a letter who match with th X and Y created by secret and string.
        Once all letters are be encoded we add the secret token to the string, so we can't lose it, and we go to use it again to decode the string.
        After the encoding we have to follow some steps to add more details to the password, like UPPERCASE Characters and Special characters.

    """

    def __init__(self):
        # Create a random string with the same length of the string
        self.__secret__ = ""

        # Get the space indexes of the original string to reorder it in the decoded string
        self.__spaceIndexes__ = []

        # Get the string length
        self.__stringLength__ = 0

        # Add random Special Chars to the encoded string to make it more difficult to decode.
        self.__dividers__ = ["$", "%", "£", "!", "@", "#", "&"]
        self.table = [
            ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a"],
            ["c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b"],
            ["d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c"],
            ["e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d"],
            ["f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
                "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e"],
            ["g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f"],
            ["h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
                "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g"],
            ["i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h"],
            ["j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1",
                "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i"],
            ["k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2",
                "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
            ["l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3",
                "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"],
            ["m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4",
                "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"],
            ["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"],
            ["o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6",
                "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"],
            ["p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7",
                "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"],
            ["q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8",
                "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"],
            ["r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q"],
            ["s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r"],
            ["t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a",
                "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s"],
            ["u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b",
                "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"],
            ["v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c",
                "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u"],
            ["w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d",
                "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v"],
            ["x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e",
                "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w"],
            ["y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f",
                "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x"],
            ["z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g",
                "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y"],
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h",
                "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            ["2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i",
                "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1"],
            ["3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2"],
            ["4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3"],
            ["5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4"],
            ["6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5"],
            ["7", "8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
                "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6"],
            ["8", "9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o",
                "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7"],
            ["9", "0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8"],
            ["0", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        ]  # List of available characters

    # Get X and Y position from the Matrix (self.table)
    def __getCoordinatesOfSecretAndLetter__(self, letter: str, secret: str):
        x, y = 0, 0  # Initialize variables

        # Set the X var to the index of letter in the first row
        x = self.table[0].index(letter)

        # For every row in the table get the first item...
        for index in range(len(self.table)):
            # ... column is made from first item of every row
            column = self.table[index][0]

            # Set the Y to the index of the row
            if secret == column:
                y = index

        # Return and array with matrix positions of the letters
        return [x, y]

    # This method is used to decrypt the letters and get the original string
    def __getCoordinatesToDecrypt__(self, letter: str, secret: str):
        x = 0  # Initialize X var to get the original Letter

        # For every list in the table...
        for i in range(len(self.table)):

            # The row is the list in the table
            row = self.table[i]

            # If the first item of the row equals to secret...
            if secret == row[0]:

                # ... set the X to the index of the letter
                x = row.index(letter)

        # Return the position of the original letter in the first row
        return x

    # Create a secret token with the same length of the string to encode the string.
    def __setSecret__(self, length: int):
        for _ in range(length):
            # Add random char to the secret while the length != string length
            self.__secret__ += self.table[0][r(0, len(self.table) - 1)]
        return 0

    # Transform string with uppercase letters and special chars
    def __transformText__(self, string: str):
        steps = 3  # Steps to add an Uppercase Letter
        signSteps = 5  # Steps to add a special char
        transformed = list(string)  # New string without special chars
        completed = []  # Final string

        for index in range(len(transformed)):
            if index % steps == 0:
                # Set the letter at this index to Uppercase
                transformed[index] = transformed[index].upper()

        # Transform the list into string
        transformed = "".join(transformed)

        for index in range(len(transformed)):
            # Create random SC (Special Char) to add to the string
            randomSign = self.__dividers__[r(0, len(self.__dividers__) - 1)]

            # If index is module of signSteps add a SC
            if index % signSteps == 0:
                # Add the letter with the SC to the final string
                completed.append(f"{transformed[index]}{randomSign}")
            else:
                # Add the letter to the final String
                completed.append(transformed[index])

        # Return the new string with SCs
        return "".join(completed)

    # Replace the SCs from the string
    def __removeSpecialCharacters__(self, string: str):
        newString = []  # Create the new string as list
        for i in range(len(string)):
            letter = string[i]  # Get the letter
            if letter in self.__dividers__:
                newString.append("")  # Remove the SC
            else:
                newString.append(letter)

        # Return the string without the SCs
        return "".join(newString)

    # Encrypt the string
    def encrypt(self, string: str):
        """
        Use this method to encode your string in E26
        """
        for i in range(len(string)):
            if string[i] == " ":
                self.__spaceIndexes__.append(i)
        string = string.split(" ")  # Remove the spaces from the string
        string = "".join(string)  # Convert the list into string
        self.__stringLength__ = len(string)  # Set the string length
        # Create the secret with the string length
        self.__setSecret__(self.__stringLength__)
        newString = ""  # Create the new string
        for i in range(self.__stringLength__):

            # Get position of the new chars
            x, y = self.__getCoordinatesOfSecretAndLetter__(
                string[i], self.__secret__[i])

            newString += self.table[y][x]  # Append the new char to the string

        newString += self.__secret__  # Add the secret token to the string
        newString = self.__transformText__(
            newString)  # Add UCs and SCs to the string
        encrypted = base64.b64encode(newString.encode("utf-8"))
        return str(encrypted, "utf-8")  # Return the encoded string

    # Decrypt the string
    def decrypt(self, string: str):
        """
        Use this method to decode your string in E26
        """
        string = base64.b64decode(string)
        string = str(string, "utf-8")
        string = self.__removeSpecialCharacters__(
            string)  # Remove the SCs from the string
        # Get the half length of the string to get secret and hashed string
        half = self.__stringLength__
        hashed = string[:half]  # Get the hashed string
        secret = string[half:half*2]  # Get the secret string
        originalString = []  # Initialize the new string
        for i in range(half):
            # Get the coordinates of secret and hadshed letter to get original letters
            x = self.__getCoordinatesToDecrypt__(
                hashed[i].lower(), secret[i].lower())
            # Add the original letters to the new string
            originalString.append(self.table[0][x])

        i = 0  # Increment when add a space

        # For index in spaceIndexes...
        for item in self.__spaceIndexes__:
            # ... set letter as the index of the space - spaces added
            letter = originalString[item - i]

            # Add a space before the letter
            letter = f" {letter}"

            # Get the index of the letter before the space
            index = originalString.index(letter[1])

            # Set the space by index on the original String
            originalString[index] = letter

            # Increment space
            i += 1

        # Return the decrypted string
        return "".join(originalString)

    def match(self, string: str, hashed: str):
        result = self.decrypt(hashed)
        if result == string:
            return True
        else:
            raise E26StringDoesNotMatchError(E26StringDoesNotMatchError.msg)


class E26Mixed(E26Hash):

    def encrypt(self, string: str):

        # Save index of spaces
        for i in range(len(string)):
            if string[i] == " ":
                self.__spaceIndexes__.append(i)  # Add index to the list

        string = string.split(" ")  # Remove the spaces from the string
        string = "".join(string)  # Convert the list into string
        self.__stringLength__ = len(string)  # Set the string length
        self.__setSecret__(self.__stringLength__)  # Create secret

        encrypted = []  # Final String
        stringList = []  # Encoded String
        secretList = []  # Secret Letters List

        for i in range(len(string)):
            x, y = self.__getCoordinatesOfSecretAndLetter__(
                string[i], self.__secret__[i])
            # Add new letter to the encoded string
            stringList.append(self.table[y][x])
            # Add new letter to the list of letters for the Secret
            secretList.append(f"{self.__secret__[i]}")

        for i in range(len(string) * 2):
            try:
                encrypted.append(stringList[i])
                encrypted.append(secretList[i])
            except:
                continue
        encrypted = self.__transformText__("".join(encrypted))
        encrypted = base64.b64encode(encrypted.encode("utf-8"))
        return str(encrypted, "utf-8")  # Return the encoded string

    def decrypt(self, string: str):
        string = base64.b64decode(string)
        string = str(string, "utf-8")
        string = self.__removeSpecialCharacters__(
            string)
        string = list(string)
        decodedString = []

        secretString = []
        encodedString = []

        for i in range(len(string)):
            if i % 2 == 0:
                encodedString.append(string[i].lower())
            else:
                secretString.append(string[i].lower())

        for i in range(len(encodedString)):
            x = self.__getCoordinatesToDecrypt__(
                encodedString[i], secretString[i])
            decodedString.append(self.table[0][x])

        return "".join(decodedString)

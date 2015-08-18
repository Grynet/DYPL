import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Stack;

/**
 * @author Tobias Kvarnström & Fredrik Nystad
 *
 */
public class NumberEncoder {

	private HashMap<Character, Integer> mappings = new HashMap<>();
	private ArrayList<String> dictionary;
	private ArrayList<String> numberList;
	private ArrayList<String> encodedNumberList;
	private String currentRemainingNumber;
	private String previousRemainingNumber;
	private boolean noMatch;
	private Stack<String[]> encodingStack;

	NumberEncoder(String dictionaryFilePath, String numberListFilePath) {
		dictionary = readFromFile(dictionaryFilePath);
		numberList = readFromFile(numberListFilePath);
		encodedNumberList = new ArrayList<String>();
		addMappings();
		noMatch = true;
	}

	private void addMappings() {
		mappings.put('e', 0);
		mappings.put('j', 1);
		mappings.put('n', 1);
		mappings.put('q', 1);
		mappings.put('r', 2);
		mappings.put('w', 2);
		mappings.put('x', 2);
		mappings.put('d', 3);
		mappings.put('s', 3);
		mappings.put('y', 3);
		mappings.put('f', 4);
		mappings.put('t', 4);
		mappings.put('a', 5);
		mappings.put('m', 5);
		mappings.put('c', 6);
		mappings.put('i', 6);
		mappings.put('v', 6);
		mappings.put('b', 7);
		mappings.put('k', 7);
		mappings.put('u', 7);
		mappings.put('l', 8);
		mappings.put('o', 8);
		mappings.put('p', 8);
		mappings.put('g', 9);
		mappings.put('h', 9);
		mappings.put('z', 9);
	}

	/**
	 * Reads a file and makes every line in the file to a String, removes all
	 * dashes and make all letters to lowerchase, then append the String to an
	 * ArrayList.
	 * 
	 * @param filePath
	 * @return ArrayList<String>
	 */
	private ArrayList<String> readFromFile(String filePath) {
		ArrayList<String> output = new ArrayList<String>();
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line = br.readLine();
			while (line != null) {
				line = line.replace("-", "");
				line = line.toLowerCase();
				output.add(line);
				line = br.readLine();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return output;
	}

	/**
	 * Converts word into a String of digits that follows the mappings.
	 * 
	 * @param word
	 * @return String
	 */
	private String wordToDigit(String word) {
		String result = "";
		for (char c : word.toCharArray()) {
			result += mappings.get(c);
		}
		return result;
	}

	/**
	 * Searches localDict for all possibly encodings of originalNumber. When it
	 * finds a match it appends the match to the global ArrayList<String>()
	 * encodedNumberList.
	 * 
	 * @param originalNumber
	 * @param localDict
	 * @return int
	 */
	private int createEncoding(String originalNumber,
			ArrayList<String[]> localDict) {
		if (currentRemainingNumber.length() == 0) {
			String result = "";
			for (String[] word : encodingStack) {
				result += word[0] + " ";
			}
			encodedNumberList.add(originalNumber + " : " + result);
		} else {
			noMatch = true;
			for (String[] word : localDict) {
				if (currentRemainingNumber.startsWith(word[1])) {
					encodingStack.push(word);
					noMatch = false;
					String temp = previousRemainingNumber;
					previousRemainingNumber = currentRemainingNumber;
					currentRemainingNumber = currentRemainingNumber
							.substring(word[1].length());
					createEncoding(originalNumber, localDict);
					currentRemainingNumber = previousRemainingNumber;
					previousRemainingNumber = temp;
					encodingStack.pop();
				}
			}
			if (noMatch) {
				return 0;
			}
		}
		return 1;

	}

	/**
	 * Returns an ArrayList containing words from the dict, and the digit form
	 * of that word, that can be created as a substring of number.
	 * 
	 * @param number
	 * @param dict
	 * @return ArrayList<String[]>
	 */
	private ArrayList<String[]> createNumberSpecificDict(String number,
			ArrayList<String> dict) {
		ArrayList<String[]> resultDict = new ArrayList<String[]>();
		for (String word : dict) {
			String digitWord = wordToDigit(word);
			if (number.contains(digitWord)) {
				String[] temp = new String[] { word, digitWord };
				resultDict.add(temp);
			}
		}
		return resultDict;
	}

	/**
	 * Starts the encoding of the numberList with help of the dictionary. Then
	 * prints out to the console all encodings.
	 */
	public void encode() {
		for (String number : numberList) {
			ArrayList<String[]> localDict = createNumberSpecificDict(number,
					dictionary);
			encodingStack = new Stack<String[]>();
			currentRemainingNumber = number;
			createEncoding(number, localDict);
		}
		for (String e : encodedNumberList) {
			System.out.println(e);
		}
	}

	public static void main(String[] args) {
		String pathToWords = args[0];
		String pathToNumbers = args[1];
		NumberEncoder encoder = new NumberEncoder(pathToWords, pathToNumbers);
		encoder.encode();
	}
}

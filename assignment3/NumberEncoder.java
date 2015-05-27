import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;


public class NumberEncoder {	
	
	private HashMap<Character, Integer> mappings = new HashMap<>();
	private ArrayList<String> words = new ArrayList<>();
	
	NumberEncoder(String filePath){
		words = readWordsFromFile(filePath);
		addMappings();
	}
		
	private void addMappings(){
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
	
	private ArrayList<String> readFromFile(String filePath){
		ArrayList<String> output = new ArrayList<String>();
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line = br.readLine();
			while (line != null) {
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
	
	
	private String wordAsNumber(String word){
		String result = "";
		for(char c : word.toCharArray()){
			result+=mappings.get(c);
		}
		return result;
	}

	private void printMatch(String number, String result, ArrayList<String> dict){
		String wordAsNumber;
		int wordLength;

		if(number.equals(""))
			System.out.println(result);
		else{
			for(word : dict){
				if(word.length > number.length)
					continue;
				wordAsNumber = wordToNumber(word);
				length = word.length
				if(number.subString(0, length).equals(wordAsNumber))				
					System.out.println(printMatch(number.SubString(length, number.length), result+=wordAsNumber));	
			}			
		}		
	}

	private ArrayList<String> createNumberSpecificDict (String number, ArrayList<String> dict){
		ArrayList<String> resultDict = new ArrayList<String>();
		for(String word : dict){
			// Word to digit form
			String newWord = ""; //"hej" = "901"
			for(char c: word.toCharArray()){
				newWord += mappings.get(c);
			}
			if (number.contains(newWord)){ 
				resultDict.add(word);
			}
		}
		return resultDict;
	}
	
			 

}



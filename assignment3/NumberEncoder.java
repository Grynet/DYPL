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
	
	private ArrayList<String> readWordsFromFile(String filePath){
		ArrayList<String> words = new ArrayList<String>();
		try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
			String line = br.readLine();
			while (line != null) {
				words.add(line);
				line = br.readLine();
			}
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return words;
	}
	
	
	private String wordAsNumber(String word){
		String result = "";
		for(char c : word.toCharArray()){
			result+=mappings.get(c);
		}
		return result;
	}

	private void printMatch(String number, String result){

		if(number.equals(""))
			System.out.println(result)
		else{

			for(word : dict){
				if(word.length > number.length)
					continue;
				wordAsNumber = wordToNumber(word);
				length = word.length
				number.subString(0, length).equals(word)	
				
				print printMatch(number.SubString(length, number.length), result+=wordAsNumber)		
			}

			
		}		
	}



	private void sort (String number, ArrayList dict){
		for(word : dict){
			// Word to digit form

			String newWord; //"hej" = "901"
			if (!number.contains(newWord)){ 
				dict.remove(word);
			}
		}
	}
	
			 

}



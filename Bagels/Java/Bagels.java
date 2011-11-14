import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;
import java.util.ArrayList;
import java.util.Scanner;

public class Bagels{
	public int size;
	private ArrayList<String> numbers;
	private HashMap<String, Integer> scores;
	private Random randomGen;
	
	public static void main(String[] args){
		Bagels b = new Bagels(3);
		b.playGame();
		
	}
	
	public Bagels(int size){
		this.size = size;
		this.numbers = new ArrayList<String>();
		this.randomGen = new Random();
		this.scores = new HashMap<String, Integer>();
	}
	
	public void playGame(){
		this.setNumbers();
		System.out.println("I am thinking of a number of length " + this.size);
		boolean gameFinished = false;
		Scanner in = new Scanner(System.in);
		String currentLine;
		ArrayList<String> parts;
		ArrayList<String> properParts;
		
		while(!gameFinished){
			System.out.print("Please enter your guess:>");
			
			currentLine = in.nextLine();
			currentLine = currentLine.trim();
			parts = new ArrayList<String>(Arrays.asList(currentLine.split("")));
			properParts = new ArrayList<String>();
			for (String part : parts){
				if (!part.equals("")){
					properParts.add(part);
				}
			}
			
			try {
				this.updateScore(properParts);
				if (this.scores.get("bagels") == 1){
					System.out.println("bagels");
				}
				else if (this.scores.get("fermi") == 3){
					System.out.println("You won!");
					gameFinished = true;
				}
				else{ 
					for (String key : this.scores.keySet()){
						for (Integer x = 0; x < this.scores.get(key); x++){
							System.out.print(key + " ");
						}
					}
				}
			} catch (Exception e) {
				// TODO Auto-generated catch block
				System.out.println(parts);
				System.out.println("OMG THAT'S SO WRONG AND STUFF.");
			}
			
			System.out.println();
		}
	}
	
	private void setNumbers(){
		String nextNumber;
		this.numbers.clear();
		
		for (int x = 0; x < this.size; x++){
			do{
				nextNumber = Integer.toString(this.randomGen.nextInt(10));
			}while (this.numbers.contains(nextNumber));
			
			this.numbers.add(nextNumber);
		}
	}
	
	private void initalizeScores(){
		this.scores.put("bagels", 0);
		this.scores.put("fermi", 0);
		this.scores.put("pico", 0);
	}
	
	public void updateScore(ArrayList<String> guess) throws Exception{
		this.initalizeScores();
		
		if (guess.size() != this.numbers.size()){
			throw new Exception("ARGHHHHHH. ARRAY SIZES DON'T MATCH");
		}
		
		String currentGuess;
		String currentItem;
		
		for (int x = 0; x < guess.size(); x++){
			currentGuess = guess.get(x);
			currentItem = this.numbers.get(x);
			
			if (currentGuess.equals(currentItem)){
				this.scores.put("fermi", this.scores.get("fermi") + 1);
			}
			else if (this.numbers.contains(currentGuess)){
				this.scores.put("pico", this.scores.get("pico") + 1);
			}
		}
		
		if ((this.scores.get("fermi") == 0) && (this.scores.get("pico")) == 0){
			this.scores.put("bagels", 1);
		}		
	}

}

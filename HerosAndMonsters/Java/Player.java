import java.util.Scanner;

public class Player{
	private char[] token;
	private int[] location;
	private Scanner in;
	
	public static void main(String[] args){
		Player p = new Player();
	}
	
	public Player(int start_x, int start_y){
		this.location = new int[2];
		this.location[0] = start_x;
		this.location[1] = start_y;
		this.token = new char[1];
		this.in = new Scanner(System.in);
		this.setPlayerToken();
	}
	
	public void setPlayerToken(){
		String nextLine = "";
		System.out.print("Please enter a token for your user :> ");
		while (true){
			nextLine = this.in.nextLine();
			if ((nextLine.length() == 1) && (!nextLine.equals(" "))){
				this.token = nextLine.toCharArray();
				break;
			}
		}		
	}
	
	public String getNextMove(){
		System.out.print("Please enter your next move :> ");
		while (true){
			nextLine = this.in.nextLine();
			if ((nextLine.length() == 1) && (!nextLine.equals("i"))){
				this.token = nextLine.toCharArray();
				break;
			}
		}	
	}
	x
	public int[] nextMove(){
		
	}
}
	

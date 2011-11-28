/*
 *      Board.java
 *      
 *      Copyright 2011 NoahNetbook <NoahNetbook@NOAHNETBOOK-PC>
 *      
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *      
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *      
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 *      
 *      
 */


public class Board {
	private char[][] board;
	private int size;
	private int start;
	private int end;
	
	
	public static void main(String[] args){
		Board b = new Board(12);
		System.out.println(b);
		b.makeMove(3, 0, 'H');
		System.out.println(b);
	}
	
	public Board(int size){
		this.size = size;
		this.start = 3;
		this.end = 6;
		this.board = new char[size][size];
		fillBoard();
	}
	
	public boolean validMove(int y, int x){
		if (this.board[x][y] == ' '){
			return true;
		}
		return false;
	}
		
	public void makeMove(int y, int x, char playerToken){
		fillBoard();
		this.board[x][y] = playerToken;
	}
	
	
	private void fillBoard(){
		for (int x = 0; x < this.size; x++){
			for (int y = 0; y < this.size; y++){
				this.board[x][y] = ' ';
			}
		}
	}
	
	public String toString(){
		String output = "";
		String border = "";
		
		for (int x = 0; x < this.size + 2; x++){
			border += "-";
		}
		
		output += border + "\n";
		
		for (int x = 0; x < this.size; x++){
			if (x != this.start){
				output += "|";
			}
			else{
				output += ">";
			}
			
			for (int y = 0; y < this.size; y++){
				output += this.board[x][y];
			}
			
			if (x != this.end){
				output += "|";
			}
			else{
				output += "<";
			}
			
			output += "\n";
		}
		
		output += border;
		
		return output;
	}
}


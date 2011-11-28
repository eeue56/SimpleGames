/*
 *      untitled.java
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
	private[][] char board;
	private int size;
	
	
	public static void main(String[] args){
		Board b = new Board(12);
		System.out.println(b);
	}
	
	public Board(int size){
		this.size = size
		this.board = new char[size][size];
		this.fillBoard();
	}
	
	private fillBoard(){
		for (int x = 0; x < this.size; x++){
			for (int y = 0; y < this.size; y++){
				this.board[x][y] = 'H';
			}
		}
	}
	
	public String toString(){
		String output = "";
		for (int x = 0; x < this.size; x++){
			for (int y = 0; y < this.size; y++){
				output += this.board[x][y];
			}
			output += "\n";
		}
		
		return output;
	}
}


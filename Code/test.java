
import java.lang.*;
import java.io.*;
import java.util.Scanner;

public class test{

	public static void main(String[] args) throws Exception {
		
		StringBuilder str = new StringBuilder("");
		try(InputStream is = new FileInputStream("cssStyle.txt");
			Scanner sc = new Scanner(is))
		{
			
			while(sc.hasNext()){
				str.append("\"" + sc.next() + "\"" +", ");
				sc.nextLine();
			}		
			
		}
		
		System.out.println(str);
	}
}
		
		
		


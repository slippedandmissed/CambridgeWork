package uk.ac.cam.jbs52.prejava.ex1;

import java.util.Scanner;

public class DetailedTest {

    private static Scanner scanner;

    private static String toBinary(long value) {
        String binary = "";
        for (int i=0; i<64; i++) {
            binary = ((value >> i & 1) == 1 ? "1": "0") + binary;
        }
        return "0b"+binary;
    }

    public static void main(String[] args) {
        scanner = new Scanner(System.in);

        System.out.print("Please enter a decimal number: ");
        long currentValue = scanner.nextLong();
        System.out.println("------------------------------");
        String command = "";
        do {
            System.out.println(toBinary(currentValue));
            System.out.print("(g)et/(s)et/(e)xit: ");
            command = scanner.next().toLowerCase().trim();
            if (command.equals("g") || command.equals("s")) {
                System.out.print("Position: ");
                int position = scanner.nextInt();
                if (command.equals("g")) {
                    System.out.println(PackedLong.get(currentValue, position));
                } else {
                    System.out.print("Value: ");
                    boolean value = scanner.nextBoolean();
                    currentValue = PackedLong.set(currentValue, position, value);
                }
            } else if (!command.equals("e")) {
                System.out.println("Unknown command: '"+command+"'");
            }
        } while (!command.equals("e"));
        scanner.close();
        System.out.println("Goodbye");
    }
}
package uk.ac.cam.jbs52.prejava.ex3;

public class ArrayLife {

    public static boolean getCell(boolean[][] world, int col, int row) {
        return
            0 <= row && row < world.length &&
            0 <= col && col < world[row].length &&
            world[row][col];
    }

    public static void setCell(boolean[][] world, int col, int row, boolean value) {
        if (0 <= row && row < world.length &&
            0 <= col && col < world[row].length) {
            world[row][col] = value;
        }
    }

    public static int countNeighbours(boolean[][] world, int col, int row) {
        int count = 0;
        for (int i=col-1; i<=col+1; i++) {
            for (int j=row-1; j<=row+1; j++) {
                if ((i != col || j != row) && getCell(world, i, j)) {
                    count++;
                }
            }
        }
        return count;
    }

    public static boolean computeCell(boolean[][] world,int col, int row) {
        boolean liveCell = getCell(world, col, row);
            
        int neighbours = countNeighbours(world, col, row);

        // The calculation below is based off the following table:

        //           | Less than 2 | 2 | 3 | More than 3
        //-----------|-------------|---|---|-------------
        // liveCell  |      0      | 1 | 1 |      0
        // !liveCell |      0      | 0 | 1 |      0

        // If and only if there are 3 neighbours and/or (there are both two neighbours and the cell is already alive) the cell survives 
            
        return neighbours == 3 || (neighbours == 2 && liveCell);
    }

    public static boolean[][] nextGeneration(boolean[][] world) {
        boolean[][] nextWorld = new boolean[world.length][world[0].length];
        for (int y=0; y<world.length; y++) {
            for (int x=0; x<world[y].length; x++) {
                boolean alive = computeCell(world, x, y);
                setCell(nextWorld, x, y, alive);
            }
        }
        return nextWorld;
    }


    public static void print(boolean[][] world) { 
        System.out.println("-"); 
        for (int row = 0; row < world.length; row++) { 
            for (int col = 0; col < world[row].length; col++) {
                System.out.print(getCell(world, col, row) ? "#" : "_"); 
            }
            System.out.println(); 
        } 
    }     

    public static void play(boolean[][] world) throws java.io.IOException {
        int userResponse = 0;
        while (userResponse != 'q') {
            print(world);
            userResponse = System.in.read();
            world = nextGeneration(world);
        }
    }

    public static boolean getFromPackedLong(long packed, int position) {
        return ((packed >>> position) & 1) == 1;
    }

    public static void main(String[] args) throws java.io.IOException {
        int size = Integer.parseInt(args[0]);
        long initial = Long.decode(args[1]);
        boolean[][] world = new boolean[size][size];
        //place the long representation of the game board in the centre of "world"
        for(int i = 0; i < 8; i++) {
            for(int j = 0; j < 8; j++) {
                world[i+size/2-4][j+size/2-4] = getFromPackedLong(initial,i*8+j);
            }
        }
        play(world);
    }
}
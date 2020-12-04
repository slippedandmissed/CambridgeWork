package uk.ac.cam.jbs52.prejava.ex2;

public class TinyLife {

    public static final int ROW_LENGTH = 8;
    public static final int COLUMN_LENGTH = 8;

    public static boolean getCell(long world, int col, int row) {
        return
            0 <= col && col < COLUMN_LENGTH &&
            0 <= row && row < ROW_LENGTH &&
            PackedLong.get(world, ROW_LENGTH*row+col);
    }

    public static long setCell(long world, int col, int row, boolean value) {
        if (0 > col || col >= COLUMN_LENGTH || 0 > row || row >= ROW_LENGTH) {
            return world;
        }
        return PackedLong.set(world, ROW_LENGTH*row+col, value);
    }

    public static int countNeighbours(long world, int col, int row) {
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

    public static boolean computeCell(long world,int col, int row) {
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

    public static long nextGeneration(long world) {
        long nextWorld = 0;
        for (int y=0; y<COLUMN_LENGTH; y++) {
            for (int x=0; x<ROW_LENGTH; x++) {
                boolean alive = computeCell(world, x, y);
                nextWorld = setCell(nextWorld, x, y, alive);
            }
        }
        return nextWorld;
    }


    public static void print(long world) { 
        System.out.println("-"); 
        for (int row = 0; row < 8; row++) { 
            for (int col = 0; col < 8; col++) {
                System.out.print(getCell(world, col, row) ? "#" : "_"); 
            }
            System.out.println(); 
        } 
    }     

    public static void play(long world) throws java.io.IOException {
        int userResponse = 0;
        while (userResponse != 'q') {
            print(world);
            userResponse = System.in.read();
            world = nextGeneration(world);
        }
    }

    public static void main(String[] args) throws java.io.IOException {
        play(Long.decode(args[0]));
    }
}
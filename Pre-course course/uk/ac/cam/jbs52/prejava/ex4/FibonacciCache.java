package uk.ac.cam.jbs52.prejava.ex4;

public class FibonacciCache {

    // Uninitialised array
    public static long[] fib = null;
 
    public static void store() throws Exception {
        if (fib == null) {
            throw new Exception("The value of 'fib' is null")    ;
        }
        
        for (int i=0; i<fib.length; i++) {
            if (i < 2) {
                fib[i] = 1;
            } else {
                fib[i] = fib[i-1] + fib[i-2];
            }
        }
    }
 
    public static void reset(int cachesize) {
        fib = new long[cachesize];
        for (int i=0; i<cachesize; i++) {
            fib[i] = 0;
        }
    }
  
    public static long get(int i) throws Exception {
        //TODO: throw an Exception with a suitable message if fib is null
        if (fib == null) {
            throw new Exception("The value of 'fib' is null")    ;
        }

        if (i < 0 || i >= fib.length) {
            throw new Exception("The index "+i+" is out of the range of the cache");
        }

        return fib[i];
    }
 
    public static void main(String[] args) {
        //TODO: catch exceptions as appropriate and print error messages
        reset(20);
        try {
            store();
            int i = Integer.decode(args[0]);
            System.out.println(get(i));    
        } catch (Exception e) {
            System.out.println(e.toString());
        }
    }
   
 }
 
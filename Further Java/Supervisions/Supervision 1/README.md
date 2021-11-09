# Further Java Supervision 1

## 1.1

A coding standard is important because it allows multiple developers to work on a shared project without worrying that their conflicting code styles will cause problems when they try to integrate their changes.

It also makes code more readable to external auditors or collaberators.

## 1.2

Importing `java.util.*` clutters the local namespace. Instead only the classes which are actually used should be imported.

The class name `wrong` should have a capital `W`.

There is no reason to redefine the constants `true` and `false`.

The method name `oldness` is a noun implying that the "oldness" is going to be calculated and returned, but it is instead printed to stdout. It should have a verblike name such as `printOldness` to make it clear it has side effects.

`oldness` should accept an `int` rather than an `Integer` because `int` is null-safe and passed by value rather than `Integer` which could be null and is passed by reference.

The argument `o` could perhaps have a more desscriptive name.

The `if` statement should be `if (!b)` or indeed `if (o <= 0)`. In the latter case, the boolean `b` can be completely removed from the program.

The first call to `System.out.println` should be indented.

The `else` block is indented inconsistently.

The `else` block needs to be surrounded by curly braces because it is more than one line long.

The first call to `System.out.print` doesn't have a semicolon at the end.

The second call to `System.out.print` should be to `System.out.println`, or indeed these two print statements could be combined into a single call to `System.out.println`. Otherwise one branch of execution of the program results in a newline but the other doesn't.

The `main` method should be `public static` rather than `static public`.

There should be a bounds check before referencing `args[0]` because if no arguments are specified this will throw an exception.

There should be a `try-catch` block to handle the potential `NumberFormatException` if the first argument is not a valid number.

`Integer.parseInt` returns an `int` rather than an `Integer` so there's no reason to autobox it.

## 1.3

### Program 1

```java
class Worker extends Thread {

    @Override
    public void run() {
        System.out.println("Working hard...");
    }

}

class Main {
  public static void main(String[] args) {
    
      Worker worker = new Worker();
      worker.start();

  }
}
```

### Program 2

```java
class Worker implements Runnable {

    @Override
    public void run() {
        System.out.println("Working hard...");
    }

}

class Main {
    public static void main(String[] args) {
        
        Worker worker = new Worker();
        Thread thread = new Thread(worker);
        thread.start();

    }
}
```

## 1.4

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Program {

	public static final String usageMessage = "Usage: \n\tjava Program user@hostname";

	public static void main(String[] args) {
		if (args.length < 1) {
			System.err.println(usageMessage);
			System.exit(1);
		}

		String[] parts = args[0].split("@");

		if (parts.length != 2) {
			System.err.println(usageMessage);
			System.exit(2);
		}

		String username = parts[0];
		String hostname = parts[1];
		int port = 79;

		try (Socket socket = new Socket(hostname, port)) {
			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

			out.println(username);

			String line;
			String response = "";
			while ((line = in.readLine()) != null) {
				response += line + "\n";
			};

			System.out.println(response);

		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
```

## 1.5

The program could fail in the following ways:
(The checked boxes represent cases that are handled)

 - [x] Not enough arguments are provided
 - [x] The argument that is provided does not have exactly one @ character
 - [ ] The provided host name might not be valid
 - [ ] The provided username might not be valid
 - [x] The connection might fail (this is handled but only prints a stack trace)

## 1.6

### a

This extract opens a socket connection to a local server running on port 10000. It then receieves a Java bytecode object from the server. It then determines the class of this object and iterates over all of the fields that instances of that class have. It prints the value of each of these fields on the receieved object.

The class has a method called "run" which is invokes in the context of the receieved object.

### b

 - Line 1 could throw an `IOException` if the connection fails
 - The call to `readObject` on line 2 could throw a `ClassNotFoundException` if the class of the serialised object could not be found
 - The same call could raise an `InvalidClassException` if there is something wrong with the class
 - The same call could raise a `StreamCorruptedException` if the control information in the stream is inconsistent
 - The same call could raise an `OptionalDataException` if the stream contains primitive data rather than an Object.
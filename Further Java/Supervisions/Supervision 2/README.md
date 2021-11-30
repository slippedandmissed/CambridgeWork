# Further Java Supervision 2

## 2.1

In this course, it is not assumed that all of the nodes in the system are known from the start, but instead an arbitrary number of new nodes are added and removed from the network during runtime.

## 2.2

For each node in either or both of the two clocks (henceforth called `current` and `incoming`), if that node is present in exactly one of the clocks, that node is set in `current` to the corresponding value from that clock. If that node exists in both clocks, that node is set in `current` to the greatest of the two corresponding values.

## 2.3

[Not sure what is meant by "complete" as the table already looks complete]

Thread S begins by calculating the new balance of A after debiting it 10, but is then pre-empted by Thread T which, uninterrupted, transfers 20 from B to A. At this point, execution returns to A which stores the balance for A it previously calculated, which doesn't include the 20 it was just given by thread T. This 20 is therefore lost. 10 is then credited to B as part of the transfer of 10 from A to B.

## 2.4

This solution is incorrect for several reasons. One is that there is no test to see if `this` has sufficient funds for the transfer. Another is that there is no check to see whether `amount` is positive.

The concurrency bug stems from the fact that since each resource is locked individually and released before the other one is acquired, the methood can be interrupted inbetween debiting from `this` and crediting `b`, which can lead to violation of the system's invariants. This should be an atomic operation.

It is difficult to test for correctness because such an interruption may occur very infrequently, and so it cn be hard to conclusively say that there is no such bug after simply not observing it for a while.

A correct implementation would acquire the lock with the smallest account number first, then the other lock, then complete the transaction, release the second lock, and then release the first one (2PL). The reason for ordering the accounts by account number is to remove the risk of deadlock.

## 2.5

### 2010 P3 Q9

a, b.

```java
class Fork {

	private boolean isHeld = false;

	public synchronized void pickUp() throws InterruptedException {
		while (isHeld) {
			wait();
		}
		isHeld = true;
	}

	public synchronized void putDown() {
		if (isHeld) {
			isHeld = false;
			notify();
		}
	}

}

class Fellow extends Thread {

	private Fork left, right;

	public Fellow(Fork left, Fork right) {
		this.left = left;
		this.right = right;
	}

	@Override
	public void run() {
		try {

			Thread.sleep(10000); // Think

			left.pickUp();
			right.pickUp();

			Thread.sleep(10000); // Eat

			left.putDown();
			right.putDown();

			Thread.sleep(10000); // Think

		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

}
```

c. This implementation might suffer deadlock if, given two forks A and B, there exists one Fellow(A,B) and another Fellow(B,A). Then, the first fellow might aquire lock A, the second fellow might acquire lock B, and then they would each wait indefinitely for the other to release their lock.

d. 

```java
class Fork implements {

	private static int forkIDCounter = 0;
	private boolean isHeld = false;
	private final int forkID;

	public Fork() {
		forkID = forkIDCounter++;
	}

	public synchronized void pickUp() throws InterruptedException {
		while (isHeld) {
			wait();
		}
		isHeld = true;
	}

	public synchronized void putDown() {
		if (isHeld) {
			isHeld = false;
			notify();
		}
	}

	public static Fork max(Fork a, Fork b) {
		return a.forkID < b.forkID ? b : a;
	}

	public static Fork min(Fork a, Fork b) {
		return a.forkID < b.forkID ? a : b;
	}

}

class Fellow extends Thread {

	private Fork left, right;

	public Fellow(Fork left, Fork right) {
		this.left = Fork.min(left, right);
		this.right = Fork.max(left, right);
	}

	@Override
	public void run() {
		try {

			Thread.sleep(10000); // Think

			left.pickUp();
			right.pickUp();

			Thread.sleep(10000); // Eat

			left.putDown();
			right.putDown();

			Thread.sleep(10000); // Think

		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

}
```

### 2011 P3 Q7

```java
public class Eval {
	public static int f(Record f) { /* ... */ }

	public static Integer maxf(Iterator<Record> it) {

		Integer m = null;
		while (it.hasNext()) {
			int v = f(it.next());
			if (m == null || m < v) {
				m = v;
			}
		}

		return m;

	}
}

abstract class Joinable implements Runnable {

	abstract void exec();

	private boolean execCompleted = false;

	public synchronized final void run() {
		exec();
		execCompleted = true;
		notify();
	}

	synchronized void join() throws InterruptedException {
		while (!execCompleted) {
			wait();
		}
	}

}

class EvalJoinable extends Joinable {

	private Integer m;
	private List<Integer> ints = new ArrayList<Integer>();

	public void addInt(Integer x) {
		ints.add(x);
	}

	public Integer getMaximum() {
		return m;
	}

	void exec() {
		m = Eval.maxf(ints.listIterator())
	}

}

Integer parmaxf(Iterator<Record> it, int n) {
		
	Thread[] threads = new Thread[n];

	for (int i=0; i<n; i++) {
		threads[i] = new Thread(new EvalJoinable());
	}

	int i=0;
	while (it.hasNext()) {
		threads[i].addInt(it.next());
		i = (i + 1) % n;
	}

	for (int i=0; i<n; i++) {
		threads[i].start();
	}

	Integer m = null;

	for (int i=0; i<n; i++) {
		threads[i].join();
		Integer n = threads[i].getMaximum()
		if (m == null || (n != null && m < n)) {
			m = n;
		}
	}

	return m;
}
```

### 2013 P3 Q7

a. A class loader is a way of programatically injecting new classes into your program at runtime. It might be used to roll out updates to network clients from a server, or to ensure that a program cannot be modified on the client-side.

A developer might need to develop their own class loader to abstract away the process of fetching the class. For example, in the code snippet given, the process of fetching the class bytecode over the network is abstracted away by the custom class loader.

b.

```java
public class Server {

	public static void main(String[] args) {

		if (args.length < 2) {
			System.err.println("Not enough arguments provided");
			System.exit(1);
		}

		if (!args[0].matches("\\+?\\d*\\.?\\d+")) {
			System.err.println("\""+args[0]+"\" is not a valid port");
			System.exit(2);
		}

		int port = Integer.parseInt(args[0]);

		ServerSocket serverSocket;
		try (serverSocket = new ServerSocket(port)) {

			Socket socket;
			while (socket = socket.accept()) {

				OutputStream os = socket.getOutputStream();

				byte[] bytes = Files.readAllBytes(Paths.get(args[1]));
				os.write(bytes);

				socket.close();

			}
		} catch (Exception e) {
			e.printStackTrace();
		}


	}

}
```

c. 

```java
public Class<?> findClass(String name) throws ClassNotFoundException {
	Socket s;
	byte[] b;
	try (s = new Socket(server, port)) {
		InputStream is = s.getInputStream();
		b = new byte[is.available()];
		is.read(b);
	} catch {
		throw new ClassNotFoundException();
	}

	return defineClass(name, b, 0, b.length);
}
```

d. 

If somebody were to gain access to the server's filesystem they could put arbitrary code into the class file. This code could then be executed on the client side.
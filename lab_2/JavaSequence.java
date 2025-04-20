import java.util.Random;

public class JavaSequence {
    public static void main(String[] args) {
        Random random = new Random();
        StringBuilder sequence = new StringBuilder();

        for (int i = 0; i < 128; i++) {
            int bit = random.nextInt(2);
            sequence.append(bit);
        }

        System.out.println(sequence.toString());
    }
}
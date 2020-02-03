
import java.io.IOException;
import java.net.URL;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
//import java.net.*;
//import java.io.IOException;
import java.io.File;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;

//class start

public class target {
    static //set arrays
     List<Double> corArray = new ArrayList<Double>();
    List<Double> avgCorrelationArray = new ArrayList<Double>();
    //set Variable for keeping time range of the current/previous time window in the correlation array.
    static int iHead = 0;
    static int iTail = 0;

    //set epoch time

    static long epoch = System.currentTimeMillis();
    static long tWinHead = epoch;
    //duration of the time window to average correlaiton
    static int durWin = 1000;//1000 msecond or 1 second
    static //durWin = 3
            //threshold for feedback
            double thres_FB = 0.2;
    //play function
    public static void playSound(final File Sound) {
        new Thread(new Runnable() {
            // The wrapper thread
            public void run() {
                try {

                    Clip clip = AudioSystem.getClip();

                    clip.open(AudioSystem.getAudioInputStream(Sound));
                    clip.start();
                    Thread.sleep(clip.getMicrosecondLength() / 1000);
                } catch (Exception e) {

                }
            }

        }).start();
    }
    //query function
    public static void queryCorr(long epoch) throws  IOException, JSONException{
        List<Double> meanCorrArrey = new ArrayList<Double>();

        String url = new Scanner(new URL("http://192.168.13.100/api/correlations/"+epoch).openStream(), "UTF-8").useDelimiter("\\A").next();
        String json =url;
        JSONObject obj = new JSONObject(json);

        JSONObject data = obj.getJSONObject("data");
        JSONObject  cross = data.getJSONObject("354708094967841");
        JSONArray crosscorrelation= cross.getJSONArray("crosscorrelations");

        for (int i = 0; i < crosscorrelation.length(); i++){
            double value = crosscorrelation.getJSONObject(i).getDouble("value");
            //System.out.println(value);
            meanCorrArrey.add(Math.abs(value));


        }
        Double meanvalue =Average(meanCorrArrey);
        corArray.add(meanvalue);
        //System.out.println(corArray);

    }



    //average in java
    public static double Average(List<Double> marks) {
        Double sum = 0.0;
        if(!marks.isEmpty()) {
            for (Double mark : marks) {
                sum = sum+ mark;
            }
            return sum.doubleValue() / marks.size();
        }
        return sum;
    }

    //correlation average function
    public static double correlationAverage() {
        List<Double> headToTail = corArray.subList(iHead, iTail);
        //System.out.println((iTail-iHead+1));
        double correlationaverage= Average(headToTail);
        //System.out.println(correlationaverage);
        return correlationaverage;
    }

    public static void main(String[] args) throws IOException, JSONException  {
        for (int i =0; i<1000000000; i++) {
            long epoch = Instant.now().toEpochMilli();
            queryCorr(epoch);
            iTail =iTail+1;


            //int size = corArray.size();
            //System.out.println(size);
            //System.out.println(iTail);
            if ( ( epoch-tWinHead)> durWin &&  iTail>iHead /*&& size> iTail-1*/) {
                //correlationAverage();
                double correlationaverage=correlationAverage();

                System.out.println("correlationaverage");
                System.out.println(correlationaverage);
                if (correlationaverage>thres_FB) {
                    playSound(new File("song.wav"));
                    System.out.println("play");
                    System.out.println(correlationaverage);
                }


                tWinHead = tWinHead + 1;
                iHead = iTail ; //ask here
                iTail = iHead;

            }

        }

    }
}

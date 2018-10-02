package s1g3_bitTorrent;

import java.io.File;
import java.net.InetAddress;
import java.util.concurrent.TimeUnit;

import org.apache.log4j.BasicConfigurator;

import com.turn.ttorrent.client.Client;
import com.turn.ttorrent.client.Client.ClientState;
import com.turn.ttorrent.client.SharedTorrent;

public class MyClient
{

    public static final String DEFAULT_TRACKER_URI = "http://localhost:6969/announce";

    public static void main(String[] args)
    {

        BasicConfigurator.configure();

        System.out.println("HOLA!");
        File output = new File("./data/");

        File torrentPath = new File("data/The-Handmaids-Tale-2x13-DivxTotaL.avi.torrent");
        //File torrentPath = new File("./data/THT.avi.torrent");
        System.out.println("TORRENT PATH "+ torrentPath.toString());
        try {
            SharedTorrent torrent = SharedTorrent.fromFile(torrentPath, output);
            System.out.println("Starting client for torrent: "+torrent.getName());
            Client client = new Client(InetAddress.getLocalHost(), torrent);

            try {
                System.out.println("Start to download: "+torrent.getName());
                client.share(); // SEEDING for completion signal
                client.download();    // DONE for completion signal

                long startTime = System.currentTimeMillis();
                while (!ClientState.SEEDING.equals(client.getState()) || !ClientState.DONE.equals(client.getState())) {

                    if (ClientState.ERROR.equals(client.getState())) {
                        throw new Exception("ttorrent client Error State");
                    }

                    System.out.printf("%f %% - %d bytes downloaded - %d bytes uploaded\n", torrent.getCompletion(), torrent.getDownloaded(), torrent.getUploaded());

                    TimeUnit.SECONDS.sleep(1);
                }
                long endTime = System.currentTimeMillis() - startTime;

                System.out.println("download completed, time  " + endTime);
            } catch (Exception e) {
                System.err.println("An error occurs...");
                e.printStackTrace(System.err);
            } finally {
                System.out.println("stop client.");
                client.stop();
            }
        } catch (Exception e) {
            System.err.println("An error occurs...");
            e.printStackTrace(System.err);
        }
    }
}

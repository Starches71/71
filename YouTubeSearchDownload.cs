using System;
using System.Threading.Tasks;
using YouTubeExplode;
using YouTubeExplode.Videos.Streams;

namespace YouTubeSearchDownload
{
    class Program
    {
        static async Task Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Usage: YouTubeSearchDownload <search_term> <output_path>");
                return;
            }

            string searchTerm = args[0]; // "Sherstin hotels Jeddah"
            string outputPath = args[1]; // Path to save the downloaded video

            var youtube = new YouTubeClient();
            
            try
            {
                Console.WriteLine($"Searching for videos related to '{searchTerm}'...");

                // Search for the term
                var searchResults = youtube.Search.GetResultsAsync(searchTerm);

                // Get the first result (for simplicity, you can expand this for more)
                var video = await searchResults.FirstAsync();

                Console.WriteLine($"Found video: {video.Title}");

                // Get the best quality stream
                var stream = await youtube.Videos.Streams.GetManifestAsync(video.Id);
                var streamInfo = stream.GetMuxedStreams().WithHighestVideoQuality();

                // Download the video
                await youtube.Videos.Streams.DownloadAsync(streamInfo, outputPath);

                Console.WriteLine($"Video downloaded successfully: {outputPath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }
}

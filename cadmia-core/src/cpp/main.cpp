#include <opencv2/opencv.hpp>

std::string video_format = "flv";
std::string server_url = "http://localhost:8080";

def start_streaming(int width, int height, int fps) {
  process = (
      ffmpeg
      .input('pipe:', format='rawvideo',codec="rawvideo", pix_fmt='bgr24', s='{}x{}'.format(width, height))
      .output(
          server_url,
          listen=1, // enables HTTP server
          pix_fmt="yuv420p",
          preset="ultrafast",
          f=video_format
      )
      .overwrite_output()
      .run_async(pipe_stdin=True)
  )
  return process;
}

int main() {
  auto cap = cv::VideoCapture(0);
  int width = int(cap.get(cv::CAP_PROP_FRAME_WIDTH));
  int height = int(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
  int fps = cap.get(cv::CAP_PROP_FPS);
  auto streaming_process = start_streaming(width, height, fps);
  
  while (true) {
    ret, frame = cap.read();
    if ret {
      streaming_process.stdin.write(frame.tobytes());
    } else {
      break;
    }
  }
      
  streaming_process.stdin.close();
  streaming_process.wait();
  cap.release();

  return 0;
}
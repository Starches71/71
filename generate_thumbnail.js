const { Img, Text, Composition, staticFile } = require('remotion');
const { render } = require('@remotion/renderer');
const fs = require('fs');

// Load the image
const imagePath = 'downloaded_images/000001.jpg';  // Adjust the path to your image

// Create a composition with the image and text overlay
const Thumbnail = () => {
  return (
    <Composition
      width={1280}
      height={720}
      fps={30}
      durationInFrames={150}  // Just a frame duration for the composition
    >
      <Img
        src={staticFile(imagePath)}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
      <Text
        text="Welcome to San Francisco!"
        fontSize={50}
        color="white"
        style={{
          position: 'absolute',
          bottom: '100px',
          left: '50%',
          transform: 'translateX(-50%)',
        }}
      />
    </Composition>
  );
};

// Render the image
async function generateThumbnail() {
  const outputPath = 'output/thumbnail_with_text.png';
  const output = await render(<Thumbnail />);

  // Save the output image
  fs.writeFileSync(outputPath, output);
  console.log('Thumbnail generated and saved to:', outputPath);
}

generateThumbnail();

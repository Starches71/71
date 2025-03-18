from manim import *

class GradientTextScene(Scene):
    def construct(self):
        # Set up the background gradient
        gradient = Rectangle(width=10, height=6)
        gradient.set_fill(WHITE, opacity=1)  # Fill with white
        gradient.set_color_by_gradient(RED, BLUE)  # Apply a gradient from red to blue
        self.add(gradient)

        # Create the text with beautiful font and styling
        text = Text("Samsung phones can now flip into two\nbecause they are the best", font="BeCine", font_size=36)
        text.set_color(WHITE)  # Set text color to white
        text.move_to(ORIGIN)  # Center the text in the scene
        
        # Add the text to the scene
        self.add(text)

        # Render the image
        self.wait(2)

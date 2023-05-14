# tkinter-image-processor
tkinter-image-processor using python


The application follows a architecture where the main functionality is encapsulated within the **_ImageProcessor_** class. The class initializes the GUI elements, and performs image processing operations, and visualizing its histogram.

**Filters** : "High Pass", "Low Pass", "Laplacian", "Median", "Salt & Pepper"
To apply filters, the class uses the ImageFilter module from the Pillow library to create filter kernels and apply them to the loaded image. The processed image is then displayed in the GUI.




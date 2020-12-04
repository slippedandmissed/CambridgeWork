package uk.ac.cam.cl.gfxintro.jbs52.entities;

import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.List;

public class TextEntity extends Entity {

	private static class ImageStrip {
		public int x;
		public int y;
		public int width;
		public int height;

		public ImageStrip(int x, int y, int width, int height) {
			this.x = x;
			this.y = y;
			this.width = width;
			this.height = height;
		}

		public Entity toCube(float blockSize, float blockDepth, float startX, float startY) {
			Entity cube = Entity.cube("text/red");
			cube.getTransform()
					.translate(startX + (width + 2*x - 1) * blockSize, startY - (height + 2*y - 1)  * blockSize, 0)
					.scale(blockSize * width, blockSize * height, blockDepth);
			return cube;
		}
	}

	public final String text;

	public int quality = 16;
	public float scale = 0.6f;
	public float depth = 0.1f;

	public TextEntity(String text) {
		this.text = text;
	}

	public void initialize() {
		BufferedImage img = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
		Graphics2D g2d = img.createGraphics();
		Font font = new Font("Arial", Font.BOLD, quality);
		g2d.setFont(font);
		FontMetrics fm = g2d.getFontMetrics();
		int width = fm.stringWidth(text);
		int height = fm.getHeight();
		g2d.dispose();

		img = new BufferedImage(width, height, BufferedImage.TYPE_INT_ARGB);
		g2d = img.createGraphics();
		g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_OFF);
		g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_NEAREST_NEIGHBOR);
		g2d.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
		g2d.setFont(font);
		fm = g2d.getFontMetrics();
		g2d.setColor(Color.WHITE);
		g2d.drawString(text, 0, fm.getAscent());
		g2d.dispose();

		int imgWidth = img.getWidth();
		int imgHeight = img.getHeight();

		List<ImageStrip> strips = new ArrayList<ImageStrip>();

		for (int x = 0; x < imgWidth; x++) {
			ImageStrip strip = new ImageStrip(x, 0, 1, 0);
			for (int y = 0; y < imgHeight; y++) {
				if (img.getRGB(x, y) != 0) {
					strip.height++;
				} else {
					if (strip.height > 0) {
						strips.add(strip);
					}
					strip = new ImageStrip(x, y+1, 1, 0);
				}
			}
			if (strip.height > 0) {
				strips.add(strip);
			}
		}
		float blockSize = scale / quality;

		float startX = -(imgWidth - 1f) * blockSize;
		float startY = (imgHeight - 1f) * blockSize;

		for (ImageStrip strip : strips) {
			if (strip.width > 0 && strip.height > 0) {
				Entity pixel = strip.toCube(blockSize, depth, startX, startY);
				pixel.setParent(this);
			}
		}

	}

}

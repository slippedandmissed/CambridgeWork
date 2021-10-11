package uk.ac.cam.cl.gfxintro.jbs52.tick1;

import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class BumpySphere extends Sphere {

	private float BUMP_FACTOR = 5f;
	private float[][] bumpMap;
	private int bumpMapHeight;
	private int bumpMapWidth;

	public BumpySphere(Vector3 position, double radius, ColorRGB colour, String bumpMapImg) {
		super(position, radius, colour);
		try {
			BufferedImage inputImg = ImageIO.read(new File(bumpMapImg));
			bumpMapHeight = inputImg.getHeight();
			bumpMapWidth = inputImg.getWidth();
			bumpMap = new float[bumpMapHeight][bumpMapWidth];
			for (int row = 0; row < bumpMapHeight; row++) {
				for (int col = 0; col < bumpMapWidth; col++) {
					float height = (float) (inputImg.getRGB(col, row) & 0xFF) / 0xFF;
					bumpMap[row][col] = BUMP_FACTOR * height;
				}
			}
		} catch (IOException e) {
			System.err.println("Error creating bump map");
			e.printStackTrace();
		}
	}

	// Get normal to surface at position
	@Override
	public Vector3 getNormalAt(Vector3 position) {
		
		Vector3 n = position.subtract(this.getPosition());
		Vector3 nhat = n.normalised();
				
		double u = Math.atan2(n.z, n.x)/(2*Math.PI);
		double v = Math.acos(n.y)/Math.PI;
		if (u < 0) {
			u += 1;
		}
				
		double sinu = Math.sin(2*Math.PI*u);
		double cosu = Math.cos(2*Math.PI*u);
		double sinv = Math.sin(Math.PI*v);
		double cosv = Math.cos(Math.PI*v);
		
		Vector3 Pu = new Vector3(-sinu*sinv, 0, cosu*sinv).normalised();
		Vector3 Pv = new Vector3(-cosu*sinv, sinv, -sinu*cosv).normalised();
		
		int bmy = (int) Math.round(v*(bumpMapHeight-1));
		int bmx = (int) Math.round(u*(bumpMapWidth-1));
		
		if (bmy >= bumpMapHeight-1) {
			bmy = bumpMapHeight-2;
		}
		if (bmx >= bumpMapWidth-1) {
			bmx = bumpMapWidth-2;
		}
		
		double Bu = bumpMap[bmy][bmx]-bumpMap[bmy][bmx+1];
		double Bv = bumpMap[bmy+1][bmx]-bumpMap[bmy][bmx];
		
		return nhat.add(n.cross(Pv).scale(-Bu).add(n.cross(Pu).scale(-Bv))).normalised();
		
	}
}

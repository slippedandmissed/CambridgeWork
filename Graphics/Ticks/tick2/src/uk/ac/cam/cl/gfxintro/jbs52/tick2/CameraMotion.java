package uk.ac.cam.cl.gfxintro.jbs52.tick2;

public class CameraMotion {

	private Camera camera;
	private float azimuth;
	private float elevation;
	private float distance;
	private float initialAzimuth;
	private float initialElevation;
	private float initialDistance;
	private long startTime;
	private long duration;
	private float lastT = -1;

	public CameraMotion(Camera camera, float azimuth, float elevation, float distance, long startTime, long duration) {
		this.camera = camera;
		this.azimuth = azimuth;
		this.elevation = elevation;
		this.distance = distance;
		this.startTime = startTime;
		this.duration = duration;
	}

	public static float timingFunction(float t) {
		return (1f - (float) Math.cos(Math.PI * t)) / 2f;
	}

	private void start() {
		this.initialAzimuth = camera.getAzimuth();
		this.initialElevation = camera.getElevation();
		this.initialDistance = camera.getDistance();
	}

	public void animate(long elapsedTime) {
		float t = ((float) (elapsedTime - startTime)) / ((float) duration);
		if (0 <= t && lastT < 0) {
			start();
		}
		if (1 < t && 1 > lastT) {
			t = 1;
		}
		lastT = t;
		if (0 <= t && t <= 1) {
			float p = timingFunction(t);
			float az = initialAzimuth + p * (azimuth - initialAzimuth);
			float el = initialElevation + p * (elevation - initialElevation);
			float dist = initialDistance + p * (distance - initialDistance);
			camera.setAzimuth(az);
			camera.setElevation(el);
			camera.setDistance(dist);
		}
	}

}

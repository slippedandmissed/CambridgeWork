package uk.ac.cam.cl.gfxintro.jbs52.entities.scenes;

import uk.ac.cam.cl.gfxintro.jbs52.entities.Entity;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.Camera;
import uk.ac.cam.cl.gfxintro.jbs52.tick2.SkyBox;

public abstract class Scene extends Entity{

	private SkyBox skybox;
	private Camera camera;

	public Scene(SkyBox skybox, Camera camera) {
		this.skybox = skybox;
		this.camera = camera;
	}
	
	public Camera getCamera() {
		return camera;
	}

	public abstract void populate();

	public void render(Camera camera, float deltaTime, long elapsedTime) {
		super.render(skybox, camera, deltaTime, elapsedTime);
	}

}

package uk.ac.cam.cl.gfxintro.jbs52.tick2;

import java.util.HashMap;

public class TextureCache {
	
	private static HashMap<String, Texture> cache = new HashMap<String, Texture>();
	
	public static Texture get(String key) {
		if (cache.containsKey(key)) {
			return cache.get(key);
		} else {
			Texture tex = new Texture();
			tex.load("resources/cubemaps/"+key+".png");
			cache.put(key, tex);
			return tex;
		}
	}

}

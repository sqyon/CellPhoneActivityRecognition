package com.sqyon.sensor.sensordatacollection;

public class SensorData {
	public String datatype;
	public boolean vis[] = new boolean[2];
	public float val[][] = new float[2][];
	public long ti[] = new long[4], avet;
	public float a, g, av, ah;
	
	SensorData() {
		for (int i = 0; i < 2; i++) {
			vis[i] = false;
			val[i] = null;
			ti[i] = 0;
		}
	}
	
	public void calc() {
//		double aa = Math.sqrt(
//				val[0][0] * val[0][0] + val[0][1] * val[0][1] + val[0][2] * val[0][2]);
//		double gg = Math.sqrt(val[1][0] * val[1][0] + val[1][1] * val[1][1] + val[1][2] *
//				val[1][2]);
//		double avv = (val[0][0] * val[1][0] + val[0][1] * val[1][1] + val[0][2] * val[1][2]) / gg;
//		double ahh = Math.sqrt(Math.abs(aa * aa - avv * avv));
		avet = 0;
		for (long i : ti)
			avet += i;
		avet /= ti.length;
//		a = (float) aa;
//		g = (float) gg;
//		av = (float) avv - g;
//		ah = (float) ahh;
	}
	
}

package com.vish.imagetotext.ocr.sample;


import android.graphics.Bitmap;
import android.os.Environment;

import com.googlecode.tesseract.android.TessBaseAPI;

import java.io.File;

public class TessOCR {
    private TessBaseAPI mTess;

    public TessOCR() {
        // TODO Auto-generated constructor stub



        mTess = new TessBaseAPI();
       // AssetManager assetManager=
        String datapath = Environment.getExternalStorageDirectory() + "/DemoOCR/";
        String language = "hin";
       // AssetManager assetManager = getAssets();
        File dir = new File(datapath + "/tessdata/");
        if (!dir.exists())
            dir.mkdirs();
        mTess.init(datapath, language,TessBaseAPI.OEM_TESSERACT_ONLY);
    }

    public String getOCRResult(Bitmap bitmap) {

        mTess.setImage(bitmap);
        String result = mTess.getUTF8Text();

        return result;
}

    public void onDestroy() {
        if (mTess != null)
            mTess.end();
    }

}

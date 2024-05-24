using System.Globalization;
using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Collections;
using IronPython.Hosting;
using Random = System.Random;
using Google.Apis.Auth.OAuth2;
using Google.Cloud.Storage.V1;
using System.Threading.Tasks;
using UnityEngine.Networking;


//using testcript.py;
//a good chunk of this code uses the OculusSensorCapture.cs from the activity detection mobile computing lab
//it is modified accordingly to work with our data and model
public class OculusSensorCapture : MonoBehaviour
{
    OculusSensorReader sensorReader;

    private StreamWriter logWriter;
    private bool isLogging = false;

    private bool inTutorial = true;

    private (string, string)[] activities = {("STD", "Standing"), ("SIT", "Sitting"),
        ("JOG", "Jogging"), ("ARC", "Arm circles"), ("STR", "Arms stretching"), ("DRI", "Driving"),
        ("TWS", "Twisting")};

    private string[] calmExercises = {
        "Nice, deep breathing! Make a graditude\nlist of 3 things you're grateful\nfor, and press A when you're done!",
        "Glad you're feeling so calm! Try\nthinking of a happy memory from\nyour childhood, and press A when\nyou're done!",
        "You're the epitome of calmness. In\nyour head, visualize yourself\ntalking to your favorite person.\nWhat do you talk about? Press A\nwhen you're done."
    };

    private string[] erraticExercises = {
        "I am so sorry you feel this way. Name\n5 things you can see, 4 things you\ntouch, 3 things you can hear, 2\nthings you can smell, and 1 thing\nyou can taste.",
        "Your breathing is very erratic. Try\nthis breathing exercise. Inhale for\n4 seconds, hold your breath for 7,\nand exhale for 8. Repeat twice more,\nand press A when you're done.",
        "Do you have a mantra you repeat when\nyou are this stressed? Repeat it to\nyourself 5 times, and press A when\nyou're done."
    };

    private string[] mood = {"Calm", "Erratic"};

    private string[] script = {
        "This is a VR meditative experience.",
        "We will measure your breathing, and\ngive you appropriate exercises\ndepending on how calm you are.",
        "Let's start by testing your breathing\nright now."
    };
    private int curExerciseIdx = 0;

    private int scriptIdx = 0;

    private int sceneIdx = 0;

    private int curTrial = 0;

    private int curActivityIdx = 0;

    private DateTime logStartTime;

    public TextMesh hudStatusText, wallStatusText, timerText;
    public TextMesh checktest;
    const string baseStatusText = "Press the front trigger\n to continue.\n";
    private string getpath;

    private string getpredcheck;
    private string getpredcheck2;
    private StorageClient storageClient;
    [SerializeField] private string bucketName = "bucket_name";
    [SerializeField] private string fileName = "myprediction.txt";

    private string serverUrl = "http://192.168.1.83:5000/";

    // Start is called before the first frame update
    void Start()
    {

        sensorReader = new OculusSensorReader();
        ProcessStartInfo start = new ProcessStartInfo();
        

        var engine = Python.CreateEngine();
        var scope = engine.CreateScope();

        
        TextAsset textAsset = Resources.Load<TextAsset>("myprediction");
        string fileContent = "sdada";
        if (textAsset != null)
        {
            // Get the text content of the file
            fileContent = textAsset.text;
        }
        else
        {
            fileContent = "ERROR";
        }

        getpredcheck = fileContent;
        //string mytextcheck = textFile.text;

        string code = "str = 'Hello world!'";

        var source = engine.CreateScriptSourceFromString(code);
        source.Execute(scope);

        //UnityEngine.Debug.Log(scope.GetVariable<string>("str"));
        checktest.text = "Welcome! \nWatch the TV, take a seat\n and press \nthe A button to continue";
        //randomNumber.text = "Random Number: " + test.random_number (1, 5);

    }


    /// <summary>
    /// Get the filename prefix of a logged data file, based on the selected activity
    /// and group member.
    /// </summary>
    string GetDataFilePrefix()
    {
        return activities[curActivityIdx].Item1;
    }

    void StartLogging()
    {
        if (inTutorial == true) {

        } else {
            curTrial += 1;

            sensorReader.RefreshTrackedDevices();

            string filename = $"{GetDataFilePrefix()}_{curTrial:D2}.csv";
            string path = Path.Combine(Application.persistentDataPath, filename);

            logWriter = new StreamWriter(path);
            logWriter.WriteLine(GetLogHeader());

            logStartTime = DateTime.UtcNow;
            hudStatusText.text = baseStatusText + "STATUS: Recording";

            var engine = Python.CreateEngine();
            var scope = engine.CreateScope();

            string code = $"str = 'Hello world!_{path}'";
            getpath = path;

            var source = engine.CreateScriptSourceFromString(code);
            source.Execute(scope);

            //UnityEngine.Debug.Log(scope.GetVariable<string>("str"));
            checktest.text = "Recording";

        }
        

    }

    void StopLogging()
    {
        if (inTutorial == true) {

        } else {
            TextAsset textAsset = Resources.Load<TextAsset>("myprediction");
            string fileContent = "sdada";

            getpredcheck = fileContent;



            
            logWriter.Close();
            string filename = $"{GetDataFilePrefix()}_{curTrial:D2}.csv";
            string path = Path.Combine(Application.persistentDataPath, filename);
            try
            {
                StartCoroutine(SendDataToServer(path));
                //ccktest.text = $"Breathing:" + getpredcheck2;
                
            } catch (Exception e)
            {
                hudStatusText.text = baseStatusText + "STATUS: Not recording" + e.Message;
            }
            //ecktest.text = $"Breathing:" + getpredcheck2

            //hudStatusText.text = baseStatusText + "STATUS: Not recording" + getpredcheck;

        }
        
        
    }

    IEnumerator SendDataToServer(string inputData)
    {
        // Create a JSON object to send to the server
        TimeSpan timeDifference = DateTime.UtcNow - logStartTime;

        timerText.text = $"{timeDifference.TotalSeconds:F2} s";

        string logValue = $"{timeDifference.TotalMilliseconds},";

        var attributes = sensorReader.GetSensorReadings();
        foreach (var attribute in attributes)
        {
            logValue += $"{attribute.Value.x},{attribute.Value.y},{attribute.Value.z},";
        }

        string fileContent = File.ReadAllText(inputData);
        string json = "{\"input\": \"" + logValue + "\"}";

        // Create a UnityWebRequest to send the data
        UnityWebRequest request = new UnityWebRequest(serverUrl, "POST");
        byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(json);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        // Send the request and wait for a response
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.ConnectionError || request.result == UnityWebRequest.Result.ProtocolError)
        {
            hudStatusText.text = baseStatusText + "STATUS: Not recording" + request.error;
            UnityEngine.Debug.LogError(request.error);
        }
        else
        {
            // Get the response from the server
            string responseText = request.downloadHandler.text;
            UnityEngine.Debug.Log("Response: " + responseText);
            
            getpredcheck = responseText;
            getpredcheck2 = responseText;
            hudStatusText.text = baseStatusText + "STATUS: Not recording";
            checktest.text = $"Breathing:" + getpredcheck2;
        }
    }


    IEnumerator SendDataToServer_CSV(string inputData)
    {
        WWWForm form = new WWWForm();
        form.AddField("appKey", "ABC"); // Add any necessary headers
        form.AddField("Content-Type", "text/csv");

        // Attach the CSV data to the form
        form.AddField("csvData", inputData);

        using (UnityWebRequest www = UnityWebRequest.Post(serverUrl, form))
        {
            yield return www.SendWebRequest();

            if (www.isNetworkError || www.isHttpError)
            {
                UnityEngine.Debug.LogError("Error uploading CSV: " + www.error);
            }
            else
            {
                UnityEngine.Debug.Log("CSV uploaded successfully!");
            }
        }

    }

    /// <summary>
    /// Fetch the header of the CSV sensor log, based on the current tracked devices,
    /// available attributes, and dimensions of each attribute.
    /// </summary>
    string GetLogHeader()
    {
        string logHeader = "time,";

        var attributes = sensorReader.GetAvailableAttributes();
        logHeader += String.Join(",", attributes);

        return logHeader;
    }

    /// <summary>Write the current sensor values to the open CSV file.</summary>
    void LogAttributes()
    {
        // Display the current time on the timer on the wall, then log it
        // in the CSV file

        
        TimeSpan timeDifference = DateTime.UtcNow - logStartTime;
        
        timerText.text = $"{timeDifference.TotalSeconds:F2} s";

        string logValue = $"{timeDifference.TotalMilliseconds},";

        var attributes = sensorReader.GetSensorReadings();
        foreach (var attribute in attributes)
        {
            logValue += $"{attribute.Value.x},{attribute.Value.y},{attribute.Value.z},";
        }

        logWriter.WriteLine(logValue);

    }

    /// <returns>The number of saved data files for the current user and activity.</returns>
    int GetNumExistingDataFiles()
    {
        var matchingFiles = Directory.GetFiles(Application.persistentDataPath, $"{GetDataFilePrefix()}*");
        return matchingFiles.Length;
    }

    /// <summary>
    /// Send a haptic vibration of the given amplitude and duration to all connected controllers.
    /// </summary>
    void SendImpulse(float amplitude, float duration)
    {
        foreach (var device in sensorReader.GetTrackedDevices())
        {
            if (device.TryGetHapticCapabilities(out var capabilities) &&
                capabilities.supportsImpulse)
            {
                device.SendHapticImpulse(0u, amplitude, duration);
            }
        }
    }
    IEnumerator WaitFor20Seconds()
    {
        UnityEngine.Debug.Log("Starting 20 second wait...");
        yield return new WaitForSeconds(20);
        UnityEngine.Debug.Log("20 seconds have passed!");
    }

    // Update is called once per frame
    void Update()
    {
        // Check which buttons on the right controller are pressed on the current frame
        bool aButtonPressed = OVRInput.GetDown(OVRInput.Button.One, OVRInput.Controller.RTouch);
        bool frontTriggerPressed = OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger, OVRInput.Controller.RTouch);

        // bool sideTriggerPressed = OVRInput.GetDown(OVRInput.Button.PrimaryHandTrigger, OVRInput.Controller.RTouch);

        // Change selected activity, send a small vibration for feedback,
        // and refresh the number of collected data files on the UI
        if (frontTriggerPressed)
        {
            if (wallStatusText.text == $"Ready to record your breathing.\nPress the front trigger to start/stop\n10 seconds of recording."){
                inTutorial = false;
                isLogging = !isLogging;
                if(isLogging)
                {
                    StartLogging();
                }
                else
                {
                    StopLogging();
                }
            } 
            
        }

        // Toggle logging on/off
        if (aButtonPressed)
        {
            //isLogging = !isLogging;
            //if (isLogging)
            //{
              //  StartLogging();
            //}
            //else
            //{
            //  StopLogging();
            //}

            sceneIdx += 1;


            // checking if scene is at a point where we are introducing the user to Sensoroom
            if(scriptIdx < 2)
            {
                wallStatusText.text = $"{script[scriptIdx]}";
                scriptIdx += 1;
            }

            // checking if scene is at a point where we are recording the user's breathing
            else if((sceneIdx % 2) != 0)
            {
                wallStatusText.text = $"Ready to record your breathing.\nPress the front trigger to start/stop\n10 seconds of recording.";
            }

            // checking if scene is at a point where we are giving the user an exercise to complete
            else if((sceneIdx % 2) == 0)
            {
                Random rnd = new Random();
                int moodIdx = rnd.Next(1);
                int exerciseIdx = (rnd.Next(1,3) - 1);
                string currMood = getpredcheck;

                if(currMood == "normal")
                {
                    wallStatusText.text = $"{calmExercises[exerciseIdx]}";
                    //StartCoroutine(WaitFor20Seconds());
                    //wallStatusText.text = $"BIG OLE TEST.";
                    //sceneIdx -=1;
                    //wallStatusText.text = e.Message;

                }
                else
                {
                    wallStatusText.text = $"{erraticExercises[exerciseIdx]}";
                    //StartCoroutine(WaitFor20Seconds());
                    //wallStatusText.text = $"BIG OLE TEST.";
                    //wallStatusText.text = e.Message;
                    
                }
            }

            SendImpulse(0.2f, 0.1f);
        }

        // Log attributes once for each frame if we are recording
        if (isLogging)
        {
            LogAttributes();
        }
    }

    /// <summary>
    /// Automatically close a log file if the app is closed while recording is in progress.
    /// Run when the scene is destroyed.
    /// </summary>
    void OnDestroy()
    {
        if (logWriter != null && logWriter.BaseStream != null)
        {
            logWriter.Close();
        }
    }

}

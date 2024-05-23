using System.Globalization;
using System;
using System.IO;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;
using System.Collections;
using System.Collections.Generic;
using IronPython.Hosting;
using UnityEngine;
using Random = System.Random;
//using testcript.py;
//a good chunk of this code uses the OculusSensorCapture.cs from the activity detection mobile computing lab
//it is modified accordingly to work with our data and model
public class OculusSensorCapture : MonoBehaviour
{
    OculusSensorReader sensorReader;

    private StreamWriter logWriter;
    private bool isLogging = false;

    private (string, string)[] activities = {("STD", "Standing"), ("SIT", "Sitting"),
        ("JOG", "Jogging"), ("ARC", "Arm circles"), ("STR", "Arms stretching"), ("DRI", "Driving"),
        ("TWS", "Twisting")};

    private string[] calmExercises = {"Nice, deep breathing! Make a graditude list of 3 things you're grateful for, and press A when you're done!",
                                    "Glad you're feeling so calm! Try thinking of a happy memory from your childhood, and press A when you're done!",
                                    "You're the epitome of calmness. In your head, visualize yourself talking to your favorite person. What do you talk about? Press A when you're done."};


    private string[] erraticExercises = {"I am so sorry you feel this way. Name 5 things you can see, 4 things you touch, 3 things you can hear, 2 tthings you can smell, and 1 think you can taste.",
                                        "Your breathing is very erratic. Try this breathing exercise. Inhale for 4 seconds, hold your breathe for 7, and exhale for 8. Repeat twice more, and press A when you're done.",
                                        "Do you have mantra you repeat when you are this stressed? Repeat it to yourself 5 times, and press A when you're done."};

    private string[] mood = {"Calm", "Erratic"};

    private string[] script = {"This is a VR meditative experience.", "We will measure your breathing, and give you appropriate exercises depending on how calm you are.", "Let's start by testing your breathing right now."};

    private int curExerciseIdx = 0;

    private int scriptIdx = 0;

    private int sceneIdx = 0;

    private int curTrial = 0;

    private int curActivityIdx = 0;

    private DateTime logStartTime;

    public TextMesh hudStatusText, wallStatusText, timerText;
    public TextMesh checktest;
    const string baseStatusText = "Press \"A\" to continue.\n";
    private string getpath;

    private string getpredcheck;

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
        checktest.text = "Welcome! \nWatch the TV and press \nthe right front trigger to continue";
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

    void StopLogging()
    {
        var engine = Python.CreateEngine();
        var scope = engine.CreateScope();

        string code = $"str = 'Coolio!'";
        //getpath = path;

        var source = engine.CreateScriptSourceFromString(code);
        source.Execute(scope);

        //UnityEngine.Debug.Log(scope.GetVariable<string>("str"));
        checktest.text = scope.GetVariable<string>("str");

        TextAsset exeAsset = Resources.Load<TextAsset>("predict_sensor_trace");
        string myerrocheck = "313";
        if (exeAsset != null)
        {
            // Create a temporary path to extract the executable
            string tempPath = Path.Combine(Application.persistentDataPath, "predict_sensor_trace" + ".exe");

            // Write the executable bytes to the temporary path
            File.WriteAllBytes(tempPath, exeAsset.bytes);

            // Start the process
            Process process = new Process();
            process.StartInfo.FileName = tempPath;
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.Arguments = getpath;
            process.StartInfo.CreateNoWindow = true; // Set to false if you want to see the console window
            process.Start();

            // Optionally wait for the process to exit
            process.WaitForExit();

            // Clean up: delete the temporary file
            File.Delete(tempPath);

            UnityEngine.Debug.Log("Process finished with exit code: " + process.ExitCode);
        }
        else
        {
            myerrocheck = "121";
        }


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



        checktest.text = $"Breathing:"+getpredcheck;
        logWriter.Close();
        hudStatusText.text = baseStatusText + "STATUS: Not recording";
        
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
                wallStatusText.text = $"Ready to record your breathing. Press the front trigger to start/stop 10 seconds of recording.";
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
                }
                else
                {
                    wallStatusText.text = $"{erraticExercises[exerciseIdx]}";
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

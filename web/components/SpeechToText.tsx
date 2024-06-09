import React, { useState } from 'react';

const SpeechToText: React.FC = () => {
    const [isRecording, setIsRecording] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    let mediaRecorder: MediaRecorder | null = null;
    let audioChunks: Blob[] = [];

    const startRecording = () => {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
                setIsRecording(true);

                // Event when audio data is available
                mediaRecorder.ondataavailable = (event: BlobEvent) => {
                    audioChunks.push(event.data);
                };

                // Event when recording is stopped
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    setAudioUrl(audioUrl);
                    audioChunks = [];  // Clear the chunks after creating the blob
                    setIsRecording(false);
                };
            })
            .catch(error => console.error('Error accessing media devices.', error));
    };

    const stopRecording = () => {
        if (mediaRecorder) {
            mediaRecorder.stop(); // This will trigger the 'stop' event
        }
    };

    return (
        <div>
            <h1>Record your speech</h1>
            <button onClick={startRecording} disabled={isRecording}>Start Recording</button>
            <button onClick={stopRecording} disabled={!isRecording}>Stop Recording</button>
            {audioUrl && <audio src={audioUrl} controls />}
        </div>
    );
};

export default SpeechToText;

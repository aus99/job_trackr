<template>
  <div class="flex">
    <div class="bg-white text-black dark:text-white w-full min-h-screen px-10">
      <div class="flex justify-between py-10 w-full">
               <div class="">
                      <h1 class="font-bold text-3xl">Your Practice Interviews</h1>
                      <h2 class="font-semibold text-xl">{{ interviews.length }} interviews conducted</h2>
               </div>
                  <button @click="toggleModal = !toggleModal" class="transition whitespace-nowrap shadow-[3px_3px_0px_0px_#000000] h-10 rounded-lg bg-cyan-600 px-4 py-2 m-1 text-sm font-medium text-white hover:bg-cyan-500 focus:outline-none">
                        New Interview
                  </button>
          <div v-if="toggleModal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed inset-0 z-50 flex justify-center items-center">
            <div class=" p-4 w-full max-w-md max-h-full">
        <!-- Modal content -->
        <div v-if="toggleModal" class="relative bg-white rounded-lg shadow dark:bg-gray-700">
            <!-- Modal header -->
            <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    Practice for an interview
                </h3>
                <button @click="toggleModal=false" type="button" class="end-2.5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
            </div>
            <!-- Modal body -->
            <div class="p-4 md:p-5">
                <form class="space-y-4">
                    <h4 class="text-xl font-normal text-gray-900 dark:text-white">Choose an application to practice an interview for:</h4>
                    <select v-model="selectedApplication"  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required>
                      <option v-for="application in applications" :value="application.id" :key="application.id">{{ application.job_title }}, {{application.company_name}}</option>
                    </select>
                    <button type="submit" v-on:click="startInterview" class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Generate Interview Questions</button>
                </form>
            </div>
        </div>
    </div>
</div>
      </div>


<div class="relative overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="px-6 py-3">
                    Job Title
                </th>
                <th scope="col" class="px-6 py-3">
                    <div class="flex items-center">
                        Company
                    </div>
                </th>
                <th scope="col" class="px-6 py-3">
                    <div class="flex items-center">
                        Completed?
                    </div>
                </th>

                <th scope="col" class="px-6 py-3">
                    <span class="sr-only">Edit</span>
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="interview in interviews" :key="interview.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <button v-if="interview.answered === false" @click="getInterviewQuestions(interview.id)" class="hover:underline">
                      {{interview.job_title}}
                  </button>
                  <a v-else :href="`/interviews/${interview.id}`" class="hover:underline">
                    {{interview.job_title}}
                  </a>
                </th>
                <td class="px-6 py-4">
                      {{interview.company_name}}
                </td>
              <td class="px-6 py-4">
                <span v-if="interview.answered === true" class="text-green-600">Yes</span>
                <span v-else class="text-red-500">No</span>
              </td>
                <td class="px-6 py-4 text-right">
                  <button v-on:click="deleteInterview(interview.id)" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>

      <!-- Interview modal -->
<div v-if="toggleInterviewModal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed inset-0 z-50 flex justify-center items-center">
    <div class="p-4 w-full max-w-md max-h-full">
        <!-- Modal content -->
        <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
            <!-- Modal header -->
            <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                    Record your answers
                </h3>
                <button @click="toggleInterviewModal=false" type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-toggle="crud-modal">
                    <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                    </svg>
                    <span class="sr-only">Close modal</span>
                </button>
            </div>
            <!-- Modal body -->


<div class="text-sm font-medium text-center text-gray-500 border-b border-gray-200 dark:text-gray-400 dark:border-gray-700">
    <ul class="flex flex-wrap justify-center -mb-px">
        <li v-for="(question, index) in questions" :key="`question-tab-${index}`" class="me-2">
          <button @click="setActiveTab(index)"
                  class="inline-block p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300"
                  :class="{'text-blue-600 border-blue-600 dark:text-blue-500 dark:border-blue-500': activeTab === index}">
            Question {{ index + 1 }}
          </button>
        </li>
      </ul>
</div>

          <div v-if="activeTab !== null">
      <div class="p-4 md:p-5">
        <h2 class="text-medium font-semibold text-gray-900 dark:text-white">{{ questions[activeTab]?.question_text }}</h2>
        <div class="mt-3 mx-3">
          <button v-if="!isRecording" @click="startRecording" class="p-2.5 group bg-gray-100 rounded-full hover:bg-gray-200 me-4 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:bg-gray-600 dark:hover:bg-gray-800" :disabled="isRecording">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-8 h-8">
              <path d="M8.25 4.5a3.75 3.75 0 1 1 7.5 0v8.25a3.75 3.75 0 1 1-7.5 0V4.5Z" />
              <path d="M6 10.5a.75.75 0 0 1 .75.75v1.5a5.25 5.25 0 1 0 10.5 0v-1.5a.75.75 0 0 1 1.5 0v1.5a6.751 6.751 0 0 1-6 6.709v2.291h3a.75.75 0 0 1 0 1.5h-7.5a.75.75 0 0 1 0-1.5h3v-2.291a6.751 6.751 0 0 1-6-6.709v-1.5A.75.75 0 0 1 6 10.5Z" />
            </svg>
          </button>
        <button v-if="isRecording" @click="stopRecording" class="p-2.5 group bg-gray-100 rounded-full hover:bg-gray-200 me-4 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:bg-gray-600 dark:hover:bg-gray-800" :disabled="!isRecording">
          <svg class="w-8 h-8 text-gray-500 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M0 0h24v24H0z" fill="none"/>
            <path d="M6 6h12v12H6z"/>
          </svg>
        </button>
          <div v-if="isRecording" class="text-right">
      {{ formatTime(recordingElapsedTime) }}/3:00
    </div>
        </div>
        <audio v-if="audioUrls[activeTab]" :src="audioUrls[activeTab]" controls class="mx-auto my-4"></audio>
      </div>

      <div class="flex justify-between items-center p-4 md:p-5">
        <!-- Previous Button -->
        <button v-if="activeTab > 0" @click="navigateTab(-1)" class="px-4 py-2 text-sm font-medium text-white bg-cyan-700 border border-gray-300 rounded-lg hover:bg-cyan-500" :disabled="activeTab === 0">
          Previous
        </button>
        <div v-else class="px-4 py-2"></div>

        <!-- Next Button -->
        <button v-if="activeTab < questions.length - 1" @click="navigateTab(1)" class="px-4 py-2 text-sm font-medium text-white bg-cyan-700 border border-gray-300 rounded-lg hover:bg-cyan-500" :disabled="activeTab === questions.length - 1">
          Next
        </button>
        <button v-else @click="submitAnswers" class="px-4 py-2 text-sm font-medium text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg" :disabled="!allAnswersRecorded">
          Submit Answers
        </button>
      </div>
    </div>
        </div>
    </div>
</div>

      <div v-if="toggleModal"  class="absolute inset-0 z-40 opacity-25 bg-black"></div>
      <div v-if="toggleInterviewModal"  class="absolute inset-0 z-40 opacity-25 bg-black"></div>
    </div>
  </div>
</template>

└<script>
import axiosClient from "@/views/axiosClient";

export default {
  data() {
    return {
      toggleModal: false,
      activeTab: 0,
      toggleInterviewModal: false,
      applications: [],
      selectedApplication: null,
      questions: [],
      interviews: [],
      selectedInterview: null,
      isRecording: false,
      recordingStartTime: null,
      recordingElapsedTime: 0,
      recordingDuration: 180,
      mediaRecorder: null,
      stopRecordingTimeout: null,
      audioBlobs: {}, // To store audio blobs for each question
      audioUrls: {}, // URLs of the recorded audios for playback
      allAnswersRecorded: false,
    }
  },
  created() {
    this.fetchApplications();
    this.getInterviews();
  },
  methods: {
    setActiveTab(index) {
      this.activeTab = index;
    },
    navigateTab(direction) {
      const nextTab = this.activeTab + direction;
      if (nextTab >= 0 && nextTab < this.questions.length) {
        this.activeTab = nextTab
        this.checkAllAnswersRecorded();
      }
    },
    fetchApplications() {
      axiosClient.get('/dashboard/list_applications/')
          .then(response => {
            this.applications = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching the applications:', error.response.data);
          });
    },
    getInterviews() {
      axiosClient.get('/interviews/get_interviews/')
          .then(response => {
            this.interviews = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching the interviews:', error.response.data);
          });
    },
    async startInterview() {
      try {
        const response = await axiosClient.post(`/interviews/start_interview/${this.selectedApplication}/`);
        console.log(response.data);
        this.getInterviews();
      } catch (error) {
        console.error(error.response.data);
      }
    },
    getInterviewQuestions(interview_id) {
      axiosClient.get(`interviews/get_interview_questions/${interview_id}/`)
          .then(response => {
            this.questions = response.data;
            this.activeTab = 0;
            this.toggleInterviewModal = true;
          })
          .catch(error => {
            console.error('There was an error fetching the interviews:', error.response.data);
          });
    },
    deleteInterview(interview_id) {
      axiosClient.delete(`/interviews/${interview_id}/delete/`)
          .then(response => {
            // Remove the interview from the local state or refresh the list
            this.getInterviews()
            console.log(response)
          })
          .catch(error => {
            console.log(error)
          });
    },
    async startRecording() {
      if (!navigator.mediaDevices) {
        alert('Recording not supported');
        return;
      }
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(stream);
        const audioChunks = [];
        this.mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, {type: 'audio/wav'});
        const audioUrl = URL.createObjectURL(audioBlob);
        // Direct assignment instead of using this.$set
        this.audioUrls[this.activeTab] = audioUrl;
        this.audioBlobs[this.activeTab] = audioBlob;
      };
        this.mediaRecorder.start();
        this.isRecording = true;
        this.recordingStartTime = Date.now();
        this.recordingElapsedTime = 0;
        this.updateRecordingTimer(); // initialize timer
        // Set up a timer to update the elapsed time every second
        this.recordingTimer = setInterval(this.updateRecordingTimer, 1000);
        if (this.stopRecordingTimeout) {
          clearTimeout(this.stopRecordingTimeout);
        }
        this.stopRecordingTimeout = setTimeout(() => {
          this.stopRecording();
        }, 180000)

        this.mediaRecorder.onerror = (event) => {
          console.error('MediaRecorder error:', event.error);
          this.stopRecording();
        }
      } catch (error) {
        console.error('Error starting audio recording:', error);
      }
    },
    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
        this.isRecording = false;
        clearInterval(this.recordingTimer);
        this.recordingStartTime = null;
        if (this.stopRecordingTimeout){
          clearTimeout(this.stopRecordingTimeout);
        }
      }
    },
    updateRecordingTimer() {
      const now = Date.now();
      this.recordingElapsedTime = Math.floor((now - this.recordingStartTime) / 1000);
      if (this.recordingElapsedTime >= this.recordingDuration) {
        this.stopRecording();
      }
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const remainingSeconds = seconds % 60;
      return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    },
    checkAllAnswersRecorded(){
      this.allAnswersRecorded = this.questions.every((question, index) => this.audioUrls[index]);
    },
    submitAnswers() {
      const audioAnswers = this.questions.map((question, index) => {
        return {
          audioBlob: this.audioBlobs[index],
          questionId: question.id
        };
      });
      this.uploadAudio(audioAnswers);
      this.toggleInterviewModal = false;
      this.getInterviews();
    },
    async uploadAudio(audioAnswers) {
      try {
        const formData = new FormData();
        audioAnswers.forEach((audioAnswer, index) => {
          formData.append(`audioBlob_${index}`, audioAnswer.audioBlob);
          formData.append(`question_id_${index}`, audioAnswer.questionId);
        });
        const response = await axiosClient.post('interviews/upload_audio_answers/', formData);
        console.log(response.data);
      } catch (error) {
        console.error('Error uploading audio URLs:', error);
      }
    },
  },
  watch: {
    audioUrls: {
      handler() {
        this.checkAllAnswersRecorded();
      },
      deep: true,
    }
  },
  mounted() {
    this.checkAllAnswersRecorded();
  }
}

</script>

<style scoped>

</style>
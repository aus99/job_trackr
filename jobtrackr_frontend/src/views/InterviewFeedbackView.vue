<template>
  <div class="bg-white p-4">
    <div class="flex flex-row items-center border-b-2 pb-3">
      <div class="">
        <h1 class="font-bold text-3xl">Feedback for interview: {{ jobDetails.job_title }} at {{jobDetails.company}}</h1>
      </div>
    </div>
          <div class="py-3 border-b-2" v-for="unit in feedback" :key="unit.question_id">
            <h2 class="font-bold text-xl">Question: </h2>
            <p class="text-lg font-medium text-gray-900 dark:text-white pb-3">{{ unit.question_text }}</p>
            <h2 class="font-bold text-xl">Your Answer: </h2>
            <p class="text-justify text-gray-500 dark:text-gray-400 pb-3">{{unit.answer_text}}</p>
            <h2 class="font-bold text-xl">Feedback: </h2>
            <p class="text-justify text-gray-500 dark:text-gray-400 pb-3">{{unit.feedback}}</p>
          </div>
  </div>
</template>

<script>
import axiosClient from "@/views/axiosClient";
export default {
    data() {
      return {
        feedback: Object,
        jobDetails: {},
      }
    },
  created() {
      this.getInterviewFeedback();
      this.getJobDetails();
  },
  methods: {
      getInterviewFeedback(){
        axiosClient.get(`/interviews/get_interview_feedback/${this.$route.params.id}/`)
            .then(response => {
              this.feedback = response.data;
            })
            .catch(error => {
              console.error('There was an error fetching the feedback:', error.response.data);
            });
      },
      getJobDetails(){
        axiosClient.get(`/interviews/get_job_details/${this.$route.params.id}/`)
            .then(response => {
              this.jobDetails = response.data;
            })
            .catch(error => {
              console.error('There was an error fetching the job details:', error.response.data);
            });
      }
  }
}
</script>

<style scoped>

</style>
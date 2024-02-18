<template>
  <div class="flex">
    <div class="bg-white text-black dark:text-white w-full min-h-screen px-10">
      <div class="flex justify-between py-10 w-full">
               <div class="">
                      <h1 class="font-bold text-3xl">Your Reports</h1>
                      <h2 class="font-semibold text-xl">{{ reports.length }} reports generated</h2>
                      <div v-if="isLoading" class="px-3 mt-3 py-3 text-xs font-medium leading-none text-center text-blue-800 bg-blue-200 rounded-full animate-pulse dark:bg-blue-900 dark:text-blue-200">Generating Report...</div>
               </div>
                  <button @click="toggleModal = !toggleModal" class="transition whitespace-nowrap shadow-[3px_3px_0px_0px_#000000] h-10 rounded-lg bg-cyan-600 px-4 py-2 m-1 text-sm font-medium text-white hover:bg-cyan-500 focus:outline-none">
                        New Report
                  </button>
          <div v-if="toggleModal" tabindex="-1" aria-hidden="true" class="overflow-y-auto overflow-x-hidden fixed inset-0 z-50 flex justify-center items-center">
            <div class=" p-4 w-full max-w-md max-h-full">
        <!-- Modal content -->
        <div v-if="toggleModal" class="relative bg-white rounded-lg shadow dark:bg-gray-700">
            <!-- Modal header -->
            <div class="flex items-center justify-between p-4 md:p-5 border-b rounded-t dark:border-gray-600">
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    Create a new report
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
                    <div>
                        <label for="title" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Job Title</label>
                        <input type="text" id="title" v-model="job_title" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
                    </div>
                    <div>
                        <label for="company" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Company</label>
                        <input type="text" id="company" v-model="company_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
                    </div>
                    <div>
                        <label for="location" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Location</label>
                        <input type="text" id="location" v-model="location" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
                    </div>
                    <button type="submit" v-on:click="createReport" class="w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Generate Report</button>
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
                    Location
                </th>

                <th scope="col" class="px-6 py-3">
                    <span class="sr-only">Edit</span>
                </th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="report in reports" :key="report.id" class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <a :href="`/reports/${report.id}`" class="hover:underline">
                    {{report.job_title}}
                  </a>
                </th>
                <td class="px-6 py-4">
                  {{ report.company_name }}
                </td>
              <td class="px-6 py-4">
                {{ report.location }}
                </td>
                <td class="px-6 py-4 text-right">
                  <button v-on:click="deleteReport(report.id)" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Delete</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
      <div v-if="toggleModal" class="absolute inset-0 z-40 opacity-25 bg-black"></div>
    </div>
  </div>


</template>

<script>


import axiosClient from "@/views/axiosClient";

export default {
  data(){
    return {
      toggleModal: false,
      job_title: '',
      company_name: '',
      location: '',
      reports: [],
      isLoading: false,
    }
  },
  created() {
    this.getReports()
  },
  methods: {
    createReport() {
      this.isLoading = true;
      axiosClient.post('/reports/create_report/', {
          job_title: this.job_title,
          company_name: this.company_name,
          location: this.location,
        })
          .then((response) => {
            console.log(response.data);
            this.getReports();
          })
      .catch((error) => {
         console.error('Error creating report:', error.response || error);
      })
      .finally(() => {
      this.isLoading = false; // Stop the loading state
      });
    },
    getReports() {
      axiosClient.get('/reports/get_reports/')
            .then(response => {
              this.reports = response.data;
            })
            .catch(error => {
              console.error('There was an error fetching the reports:', error.response.data);
            });
    },
    deleteReport(report_id) {
      axiosClient.delete(`/reports/${report_id}/delete/`)
          .then(response => {
            // Remove the application from the local state or refresh the list
            this.getReports()
            console.log(response)
          })
          .catch(error => {
            console.log(error)
          });
    }
  },
}
</script>

<style src="../index.css">

</style>
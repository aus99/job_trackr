

<template>
  <div class="flex">
    <div class="bg-white text-black dark:text-white w-full min-h-screen">
            <div class="flex justify-between py-10 w-full">
               <div class="px-16">
                      <h1 class="font-bold text-3xl">Your Submitted Applications</h1>
                      <h2 class="font-semibold text-xl">{{applications.length}} applications submitted</h2>
               </div>
               <div class="mx-16">
                  <button @click="toggleModal = !toggleModal" class="transition whitespace-nowrap shadow-[3px_3px_0px_0px_#000000] rounded-lg bg-cyan-600 px-4 py-2 m-1 text-sm font-medium text-white hover:bg-cyan-500 focus:outline-none">
                        New Application
                  </button>
                </div>
            </div>
      <div class="flex justify-center items-start py-3 px-8">
    <!-- Search input -->
    <input
      v-model="searchQuery"
      @input="filterApplications"
      class="block h-11 w-3/4 rounded-md border-gray-300 text-base leading-5 transition focus:border-primary-base focus:outline-none focus:ring-4 focus:ring-primary-lightest mx-2"
      data-testid="custom-search"
      placeholder="Search for roles or companies"
      type="search"
    >

    <!-- Status dropdown -->
    <div class="relative inline-block text-left h-11 w-1/4 mx-2">
      <button @click="toggleDropdown" class="inline-flex justify-between w-full h-full px-4 py-2 bg-white text-base text-gray-500 border rounded-md focus:border-primary-base focus:outline-none focus:ring-4 focus:ring-primary-lightest">
        {{ selectedStatus || 'Status' }}
        <svg height="20" width="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false" class="css-8mmkcg">
          <path d="M4.516 7.548c0.436-0.446 1.043-0.481 1.576 0l3.908 3.747 3.908-3.747c0.533-0.481 1.141-0.446 1.574 0 0.436 0.445 0.408 1.197 0 1.615-0.406 0.418-4.695 4.502-4.695 4.502-0.217 0.223-0.502 0.335-0.787 0.335s-0.57-0.112-0.789-0.335c0 0-4.287-4.084-4.695-4.502s-0.436-1.17 0-1.615z"></path>
        </svg>
      </button>

      <!-- Dropdown menu -->
      <div v-if="showDropdown" class="origin-top-right absolute right-0 mt-2 w-56 rounded-md z-10 shadow-lg bg-white ring-1 ring-black ring-opacity-5">
        <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
          <a href="#" v-for="status in statusOptions" :key="status" @click.prevent="selectStatus(status)" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100" role="menuitem">
            {{ status }}
          </a>
        </div>
      </div>
    </div>
  </div>



      <div class="mb-4 overflow-hidden  bg-white">
        <div v-for="application in filteredApplications" :key="application.id" class="bg-gray-100 w-11/12 cursor-pointer rounded shadow hover:bg-emerald-50 mx-8 rounded-xl my-2">
  <div class="block p-4 transition duration-150 ease-in-out hover:bg-primary-lightest focus:outline-none "  @click="selectApplication(application)">
    <div class="flex items-center">
      <div class="flex w-full flex-1 flex-col items-center md:w-auto md:flex-row">
        <div class="mb-2 flex w-full shrink-0 items-center justify-center md:mb-0 md:w-auto">
          <div class="h-16 w-16 shrink-0">
            <span style="box-sizing: border-box; display: inline-block; overflow: hidden; width: 64px; height: 64px; background: none; opacity: 1; border: 0px; margin: 0px; padding: 0px; position: relative;">
              <img alt="PwC" src="https://storage.googleapis.com/simplify-imgs/companies/default/logo.png" decoding="async" data-nimg="fixed" class="rounded-md" style="position: absolute; inset: 0px; box-sizing: border-box; padding: 0px; border: none; margin: auto; display: block; width: 0px; height: 0px; min-width: 100%; max-width: 100%; min-height: 100%; max-height: 100%;">
            </span>
          </div>
          <div class="ml-4 w-full truncate md:min-w-3xs md:max-w-3xs lg:min-w-xs lg:max-w-xs xl:min-w-lg xl:max-w-lg">
            <div class="w-48 truncate text-left text-base font-medium leading-5 text-gray-600">{{ application.job_title }}</div>
            <p class="mt-1 items-center truncate text-left text-sm leading-5 text-gray-500 grid-cols-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 -mt-1 mr-1 inline-block">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
              </svg>
              {{ application.company_name }}
            </p>
            <p class="mt-1 items-center truncate text-left text-sm leading-5 text-gray-500 grid-cols-2">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 -mt-1 mr-1 inline-block">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
              </svg>
              {{ application.location }}
            </p>
          </div>
        </div>
        <div class="mx-4 w-full flex-1 items-center md:mr-0 lg:ml-8">





      <div class="p-5">
        <div class="mx-4 p-4">
           <div class="flex items-center">
            <div class="flex items-center relative">
                <div class="rounded-full transition duration-500 ease-in-out h-12 w-12 py-3 border-2" :class="getStepClass(application.status, 'applied')">
                    <svg xmlns="http://www.w3.org/2000/svg" height="100%" width="100%" viewBox="0 0 512 512" stroke="currentColor" :fill="['rejected', 'applied'].includes(application.status) ? '#ffffff' : '#0097A7'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bookmark "><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16.1 260.2c-22.6 12.9-20.5 47.3 3.6 57.3L160 376V479.3c0 18.1 14.6 32.7 32.7 32.7c9.7 0 18.9-4.3 25.1-11.8l62-74.3 123.9 51.6c18.9 7.9 40.8-4.5 43.9-24.7l64-416c1.9-12.1-3.4-24.3-13.5-31.2s-23.3-7.5-34-1.4l-448 256zm52.1 25.5L409.7 90.6 190.1 336l1.2 1L68.2 285.7zM403.3 425.4L236.7 355.9 450.8 116.6 403.3 425.4z"/>
                    </svg>
                </div>
                <div class="absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase"
                      :class="{ 'text-cyan-600': application.status === 'applied','text-gray-500': application.status !== 'applied', 'text-red-600': application.status === 'rejected' }">APPLIED</div>
            </div>
            <div class="flex-auto border-t-2 transition duration-500 ease-in-out"
                  :class="getStepClass(application.status, 'screening')"></div>
            <div class="flex items-center text-white relative">
                <div class="rounded-full transition duration-500 ease-in-out h-12 w-12 py-3 border-2" :class="getStepClass(application.status, 'screening')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user-plus ">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m5.231 13.481L15 17.25m-4.5-15H5.625c-.621 0-1.125.504-1.125 1.125v16.5c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9zm3.75 11.625a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
                    </svg>
                </div>
                <div class="absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase"
                      :class="{ 'text-cyan-600': application.status === 'screening','text-gray-500': application.status !== 'screening', 'text-red-600': application.status === 'rejected' }">SCREENING</div>
            </div>
            <div class="flex-auto border-t-2 transition duration-500 ease-in-out"
                  :class="getStepClass(application.status, 'interview')"></div>
            <div class="flex items-center text-gray-500 relative">
                <div class="rounded-full transition duration-500 ease-in-out h-12 w-12 py-3 border-2" :class="getStepClass(application.status, 'interview')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-mail ">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" /><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
                    </svg>
                </div>
                <div class="absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase"
                      :class="{ 'text-cyan-600': application.status === 'interview','text-gray-500': application.status !== 'interview', 'text-red-600': application.status === 'rejected' }">INTERVIEW</div>
            </div>
            <div class="flex-auto border-t-2 transition duration-500 ease-in-out"
                 :class="getStepClass(application.status, 'offer')"></div>
            <div class="flex items-center text-gray-500 relative">
                <div class="rounded-full transition duration-500 ease-in-out h-12 w-12 py-3 border-2" :class="getStepClass(application.status, 'offer')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-database ">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M11.35 3.836c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m8.9-4.414c.376.023.75.05 1.124.08 1.131.094 1.976 1.057 1.976 2.192V16.5A2.25 2.25 0 0118 18.75h-2.25m-7.5-10.5H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V18.75m-7.5-10.5h6.375c.621 0 1.125.504 1.125 1.125v9.375m-8.25-3l1.5 1.5 3-3.75" />
                    </svg>
                </div>
                <div class="absolute top-0 -ml-10 text-center mt-16 w-32 text-xs font-medium uppercase"
                      :class="{ 'text-cyan-600': application.status === 'offer', 'text-gray-500': application.status !== 'offer', 'text-red-600': application.status === 'rejected'}">OFFER</div>
            </div>
        </div>



      </div>

    </div>
        </div>

      </div>

    </div>

  </div>
          <!-- Expandable Details -->
            <div v-if="activeApplication === application" :class="{'transition duration-150 ease-in-out': activeApplication === application}" class="border-t border-gray-200 " @click.stop="activeApplication = application">
        <form class="p-8">
    <div class="grid gap-6 mb-6 md:grid-cols-3">
        <div>
            <label for="job_title"  class="block mb-2 text-sm font-medium text-gray-900 dark:text-white text-left">Job Title</label>
            <input type="text" v-model="editableApplication.job_title" id="job_title" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
        </div>
        <div>
            <label for="company" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white text-left">Company</label>
            <input type="text" id="company" v-model="editableApplication.company_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
        </div>
        <div>
            <label for="location" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white text-left">Location</label>
            <input type="text" v-model="editableApplication.location" id="location" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
        </div>
        <div>
            <label for="application_status" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white text-left">Application Status</label>
        <select id="application_status" v-model="editableApplication.status" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required>
          <option value="applied">Applied</option>
          <option value="screening">Screening</option>
          <option value="interview">Interview</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
        </select>
        </div>

    </div>
          <div class="mb-6 ">

            <label for="job_description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white text-left">Job Description</label>
            <textarea id="job_description" v-model="editableApplication.description" rows="4" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Paste job description..." required></textarea>

          </div>

                <div class="flex-items justify-end mt-1 sm:mt-0 sm:flex sm:space-x-3">
                <button type="submit" v-on:click="deleteApplication" class="text-red-600 inline-flex items-center hover:text-white border border-red-600 hover:bg-red-600 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900">
                  <svg class="w-5 h-5 mr-1 -ml-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path></svg>
                  Delete
              </button>
                  <button type="submit" v-on:click="updateApplication"  class="text-white bg-cyan-700 hover:bg-cyan-500 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center">  Update  </button>
                </div>
  </form>
      </div>


</div>


          </div>
      <div v-if="toggleModal" class="fixed overflow-x-auto overflow-y-auto inset-0 flex items-center z-50">
          <div class="h-full w-full p-20 items-center justify-center">
            <div class="bg-white w-full rounded shadow-2xl flex flex-col w-full">
              <h2 class="text-xl font-semibold leading-6 text-gray-900 bg-primary-light pt-8 pl-8 rounded-t">Add New Application</h2>
              <form class="p-8 w-full">
    <div class="grid gap-6 mb-6 md:grid-cols-2">
        <div>
            <label for="job_title"  class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Job Title</label>
            <input type="text" v-model="job_title" id="job_title" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
        </div>
        <div>
            <label for="last_name" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Company</label>
            <input type="text" id="company" v-model="company_name" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
        </div>
        <div>
            <label for="company" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Location</label>
            <input type="text" v-model="job_location" id="location" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="" required>
        </div>
        <div>
            <label for="application_status" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Application Status</label>
        <select id="application_status" v-model="application_status" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" required>
          <option selected>Applied</option>
          <option value="applied">Applied</option>
          <option value="screening">Screening</option>
          <option value="interview">Interview</option>
          <option value="offer">Offer</option>
          <option value="rejected">Rejected</option>
        </select>
        </div>
    </div>
                <div class="mb-6">

<label for="job_description" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Job Description</label>
<textarea id="job_description" v-model="job_description" rows="4" class="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Paste job description..." required></textarea>

                </div>
                <div class="grid gap-2 mb-3 md:grid-cols-2">
                <button @click="toggleModal=false" class="inline-flex w-full justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-base font-medium leading-6 text-gray-700 shadow-sm transition duration-150 ease-in-out hover:text-gray-500 focus:border-primary-base focus:outline-none focus:ring-4 focus:ring-primary-lightest sm:text-sm sm:leading-5">
            Close
          </button>
                  <button type="submit" v-on:click="addApplication" class="text-white bg-cyan-700 hover:bg-cyan-500 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center">Add</button>
                </div>
  </form>

            </div>
          </div>
      </div>
      <div v-if="toggleModal" class="absolute inset-0 z-40 opacity-25 bg-black"></div>
      </div>
  </div>



</template>

<script>
  import axiosClient from "@/views/axiosClient";

  export default {
    data() {
      return {
        toggleModal: false,
        job_title: '',
        company_name: '',
        job_location: '',
        application_status: '',
        job_description: '',
        applications: [],
        activeApplication: null,
        editableApplication: {},
        selectedStatus: null,
        showDropdown: false,
        statusOptions: ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected'],
      }
    },
    created() {
      this.fetchApplications();
    },
    methods: {
      addApplication() {
        axiosClient.post('/dashboard/new_application/', {
          job_title: this.job_title,
          company_name: this.company_name,
          job_location: this.job_location,
          application_status: this.application_status,
          job_description: this.job_description,
        })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.log(error.data);
          });
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
      selectApplication(application) {
        this.activeApplication = this.activeApplication === application ? null : application;
        this.editableApplication = Object.assign({}, application)
      },
      deleteApplication() {
        axiosClient.delete(`/dashboard/${this.activeApplication.id}/delete/`)
        .then(response => {
        // Remove the application from the local state or refresh the list
        this.applications = this.applications.filter(app => app.id !== this.activeApplication.id);
        console.log(response)
    })
    .catch(error => {
      console.log(error)
    });
      },
      updateApplication() {
        if (this.editableApplication && this.editableApplication.id){
          axiosClient({
          method: "put",
          url: `/dashboard/${this.editableApplication.id}/update/`,
          data: {
            job_title: this.editableApplication.job_title,
            company_name: this.editableApplication.company_name,
            job_location: this.editableApplication.location,
            application_status: this.editableApplication.status,
            job_description: this.editableApplication.description,
          }
        })
          .then((response) => {
            console.log(response.data);
          })
          .catch((error) => {
            console.log(error.data);
          });
        }
      },
  getStepClass(status, currentStep) {
    const order = ['applied', 'screening', 'interview', 'offer'];
    const currentIndex = order.indexOf(status);
    const stepIndex = order.indexOf(currentStep);

    if (stepIndex < currentIndex) {
      // This is a previous step
      return 'text-cyan-600 bg-white border-cyan-600';
    } else if (status === 'rejected'){
      return 'text-white border-red-500 bg-red-500'
    }
    else if (stepIndex === currentIndex) {
      // This is the current step
      return 'text-white bg-cyan-600 border-cyan-600';
    } else {
      // This is a subsequent step
      return 'text-gray-500 bg-white border-gray-300';
    }
  },
      toggleDropdown(){
        this.showDropdown = !this.showDropdown;
      },
      selectStatus(status){
        this.selectedStatus = status;
        this.showDropdown = false;
      }
    },
    computed: {
    filteredApplications() {
      let filtered = this.applications;

      if (this.selectedStatus) {
        filtered = filtered.filter(app => app.status.toLowerCase() === this.selectedStatus.toLowerCase());
      }

      if (this.searchQuery) {
        filtered = filtered.filter(app => app.job_title.toLowerCase().includes(this.searchQuery.toLowerCase()) || app.company_name.toLowerCase().includes(this.searchQuery.toLowerCase()));
      }

      return filtered;
    },
  }
  };
</script>

<style src="../index.css">

</style>

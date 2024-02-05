<template>
  <div class="bg-white p-4 shadow">
    <div class="flex flex-row items-center pb-3 border-b-2">
      <div class="relative h-20 w-20 shrink-0 rounded-md sm:h-28 sm:w-28 2xl:h-32 2xl:w-32">
        <span style="box-sizing: border-box; display: block; overflow: hidden; width: initial; height: initial; background: none; opacity: 1; border: 0px; margin: 0px; padding: 0px; position: absolute; inset: 0px;">
          <img alt="Company Logo" :src="report.logo" class="rounded-md" style="position: absolute; inset: 0px; box-sizing: border-box; padding: 0px; border: none; margin: auto; display: block; width: 0px; height: 0px; min-width: 100%; max-width: 100%; min-height: 100%; max-height: 100%; object-fit: contain;">
        </span>
      </div>
      <div class="ml-4 text-left xl:ml-8"><p class="text-xl font-semibold sm:text-2xl">{{ report.company_name }}</p>
        <p class="mt-1 text-xs text-gray-600 sm:text-sm">{{report.job_title}}</p>
        <div class="mb-2 flex flex-wrap gap-x-2 text-xs"><div class="mt-2 rounded-full bg-gray-100 px-2 py-1 sm:p-2">
          {{ report.sector }}</div>
        </div>
        <div class="mt-2 flex justify-start space-x-1 text-xs md:space-x-2 lg:space-x-1 2xl:space-x-2"><a class="flex items-center space-x-2 rounded-2xl border border-solid border-stone-200 px-2 py-1 text-stone-600 hover:border-stone-600 hover:text-stone-800" :href="fullWebsiteUrl" rel="nofollow" target="_blank"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" aria-hidden="true" class="mr-1" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
        </svg>Website</a>
        </div>
      </div>
    </div>
    <div class="mt-3">
      <div class="rounded-xl">
        <div class="grid grid-cols-1 divide-y-2">
          <div class="mb-3"><div class="text-left">
            <div class=" text-base font-semibold">Company Overview</div>
            <div class="mt-3 text-sm">{{report.description}}</div></div><div class=""><div class="mb-1 flex flex-wrap gap-x-2 text-xs ">
              </div>
            </div>
          </div>
          <div class="py-5 text-left">
            <div class="grid grid-cols-5 divide-x-2">
              <div class="text-center"><h3 class="text-xs">Minimum Salary</h3>
                <h1 class="text-sm sm:text-lg xl:text-xs font-bold">{{ report.min_salary }}</h1>
              </div>
              <div class="text-center">
                <h3 class="text-xs">Maximum Salary</h3>
                <h1 class="text-sm sm:text-lg xl:text-xs font-bold">{{ report.max_salary }}</h1>
              </div>
              <div class="text-center">
                <h3 class="text-xs">Average Salary</h3>
                <h1 class="text-sm sm:text-lg xl:text-xs font-bold">{{ report.median_salary }}</h1>
              </div><div class="text-center">
              <h3 class="text-xs">Currency</h3>
              <h1 class="text-sm sm:text-lg xl:text-xs font-bold"> {{ report.salary_currency }}</h1>
            </div>
              <div class="text-center">
              <h3 class="text-xs">Location</h3>
              <h1 class="text-sm sm:text-lg xl:text-xs font-bold"> {{ report.location }}</h1>
            </div>
            </div>
          </div>

          <div class="text-left"><div class="mt-3 text-base font-semibold">Relevant Projects</div>
            <div class="my-3 text-sm">{{report.projects}}
            </div>
          </div>
          <div class="text-left">
            <div class="mt-3 text-base font-semibold">Latest News</div>
            <div class="my-3 text-sm">
              <ul>
        <li v-for="news in report.news_list" :key="news.id" class="mb-2 ml-5 list-disc">
          <a :href="news.url" class="text-blue-500 hover:text-blue-600">{{ news.title }}</a>
          <p>{{ news.snippet }}</p>
        </li>
      </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosClient from "@/views/axiosClient";

export default {
  data(){
    return {
      report : Object
    }
  },
  created() {
    this.getReport()
  },
  computed: {
  fullWebsiteUrl() {
    if (this.report.website_url.startsWith('http://') || this.report.website_url.startsWith('https://')) {
      return this.report.website_url;
    }
    return `https://${this.report.website_url}`;
  }
},
  methods: {
    getReport() {
      axiosClient.get(`/reports/${this.$route.params.id}/`)
            .then(response => {
              this.report = response.data;
            })
            .catch(error => {
              console.error('There was an error fetching the report:', error.response.data);
            });
    },
  }
}
</script>

<style src="../index.css">

</style>
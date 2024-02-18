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
          <div class="text-left">
            <div class="mt-3 text-base font-semibold">Top Reviews</div>

<figure v-for="review in report.top_reviews" :key="review.author_name" class="max-w-screen-md my-2">
    <blockquote>
        <p class="text-base font-semibold text-gray-900 dark:text-white">"{{review.text}}"</p>
    </blockquote>
    <figcaption class="flex items-center mt-3 space-x-3 rtl:space-x-reverse">
        <div class="flex items-center divide-x-2 rtl:divide-x-reverse divide-gray-300 dark:divide-gray-700">
            <cite class="pe-3 font-medium text-gray-700 dark:text-white">{{ review.author_name }}</cite>
        </div>
    </figcaption>
  <div class="flex items-center my-4 text-yellow-300">
    <div v-for="star in 5" :key="star" class="w-5 h-5 me-1">
      <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
            <path v-if="star <= review.rating" d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
            <path v-else d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" class="text-gray-300"/>
        </svg>
    </div>
  </div>
</figure>

          </div>
          <div class="text-left">
            <div class="mt-3 text-base font-semibold">Overall Ratings</div>


<div class="flex items-center mb-2">
    <div class="flex items-center my-4 text-yellow-300">
    <div v-for="star in 5" :key="star" class="w-5 h-5 me-1">
      <svg aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 22 20">
            <path v-if="star <= report.overall_rating" d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z"/>
            <path v-else d="M20.924 7.625a1.523 1.523 0 0 0-1.238-1.044l-5.051-.734-2.259-4.577a1.534 1.534 0 0 0-2.752 0L7.365 5.847l-5.051.734A1.535 1.535 0 0 0 1.463 9.2l3.656 3.563-.863 5.031a1.532 1.532 0 0 0 2.226 1.616L11 17.033l4.518 2.375a1.534 1.534 0 0 0 2.226-1.617l-.863-5.03L20.537 9.2a1.523 1.523 0 0 0 .387-1.575Z" class="text-gray-300"/>
        </svg>
    </div>
    <p class="ms-1 text-sm font-medium text-gray-500 dark:text-gray-400">{{ report.overall_rating }}</p>
    <p class="ms-1 text-sm font-medium text-gray-500 dark:text-gray-400">out of</p>
    <p class="ms-1 text-sm font-medium text-gray-500 dark:text-gray-400">5</p>
  </div>
  </div>
<p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ report.total_reviews }} reviews</p>
<div v-for="star in [5, 4, 3, 2, 1]" :key="star" class="flex items-center mt-4">
    <a href="#" class="text-sm font-medium text-blue-600 dark:text-blue-500 hover:underline">{{ star }} star</a>
    <div class="w-2/4 h-5 mx-4 bg-gray-200 rounded dark:bg-gray-700">
        <div class="h-5 bg-yellow-300 rounded" :style="{ width: ratingDistribution[star] + '%' }"></div>
    </div>
    <span class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ calculateDistribution(report.overall_rating)[star] }}%</span>
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
  },
    ratingDistribution() {
    return this.calculateDistribution(this.report.overall_rating);
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
    calculateDistribution(averageRating) {
    const distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0};
    const totalPercentage = 100;
    const distributionStep = totalPercentage / (Object.keys(distribution).length - 1);

    for (let rating = 1; rating <= 5; rating++) {
      const distanceFromAvg = Math.abs(averageRating - rating);
      distribution[rating] = Math.max(0, totalPercentage - (distanceFromAvg * distributionStep));
    }

    let sumDistribution = Object.values(distribution).reduce((a, b) => a + b, 0);
    for (let rating in distribution) {

      distribution[rating] = Math.ceil((distribution[rating] / sumDistribution) * 100);
    }


    sumDistribution = Object.values(distribution).reduce((a, b) => a + b, 0);
    if (sumDistribution > 100) {

      const ratingsDescending = Object.keys(distribution).sort((a, b) => distribution[b] - distribution[a]);
      for (let rating of ratingsDescending) {
        const excess = sumDistribution - 100;
        if (excess > 0 && distribution[rating] > 0) {
          distribution[rating] -= excess;
          break;
        }
      }
    }

    return distribution;
  },
  }
}
</script>

<style src="../index.css">

</style>
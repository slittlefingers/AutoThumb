import React from 'react';

const ActionDetail = ({ thinking, action, operation }) => {
  return (
    <div className="flex flex-col items-center justify-center w-full h-full transition-opacity duration-500 ease-in-out">
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <img src="/action.png" alt="operation" class="w-1/6 h-1/8 pl-2" />
              <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                ACTION
              </h5>
              <p class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1">
                Action{action}
              </p>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <img src="/operation.png" alt="operation" class="w-1/6 h-1/8" />
              <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                OPERATION
              </h5>
              <p class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1">
                {operation}
              </p>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      <div class="relative mt-6 flex w-96 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="p-6">
              <img src="/thinking.png" alt="operation" class="w-1/6 h-1/8" />
              <h5 class="mb-2 block font-sans text-xl font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased pl-1 pt-2">
                THINKING
              </h5>
              <p class="block font-sans text-base font-light leading-relaxed text-inherit antialiased pl-1">
                {thinking}
              </p>
            </div>
            <div class="p-1 pt-0"></div>
      </div>
      </div>
  );
};

export default ActionDetail;

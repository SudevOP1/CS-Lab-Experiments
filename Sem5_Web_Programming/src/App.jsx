// import React from 'react'
import ak47 from "./assets/ak47.png"
import cat from "./assets/cat.png"

let Card = ({ classNames="", text="", img=null }) => {
  return (
    <div className={`flex flex-col justify-center items-center px-10 py-8 bg-slate-800 rounded-3xl`}>
      <img src={img} className={`${classNames}`} />
      <p className={`text-white font-semibold text-4xl w-full text-center ${img?"mt-8 pt-8 border-t-2 border-blue-500":""}`}>{text}</p>
    </div>
  )
}

let App = () => {
  return (
    <div className='min-h-screen w-full flex flex-wrap gap-10 items-center justify-center bg-slate-950 p-20'>
      <Card text='ak47' img={ak47} classNames="w-100 h-100" />
      <Card text='cat' img={cat} classNames="w-100 h-100" />
      <Card text='ak47' img={ak47} classNames="w-100 h-100" />
      <Card text='cat' img={cat} classNames="w-100 h-100" />
      <Card text='ak47' img={ak47} classNames="w-100 h-100" />
      <Card text='cat' img={cat} classNames="w-100 h-100" />
      <Card text='ak47' img={ak47} classNames="w-100 h-100" />
      <Card text='cat' img={cat} classNames="w-100 h-100" />
    </div>
  )
}

export default App

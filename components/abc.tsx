import { motion } from "framer-motion";
import { FaTools } from "react-icons/fa";

const PageUnderConstruction = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white text-center px-4">
      <motion.div
        initial={{ rotate: 0 }}
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 3, ease: "linear" }}
        className="text-6xl text-yellow-400 mb-4"
      >
        <FaTools />
      </motion.div>

      <h1 className="text-4xl font-bold">Page Under Construction</h1>
      <p className="text-lg mt-2 text-gray-400">
        We're working hard to bring you something amazing. Stay tuned! 🚀
      </p>

      <div className="mt-6">
        <button className="bg-yellow-400 text-gray-900 px-6 py-2 rounded-lg font-semibold hover:bg-yellow-500 transition duration-300">
          Back to Home
        </button>
      </div>
    </div>
  );
};

export default PageUnderConstruction;
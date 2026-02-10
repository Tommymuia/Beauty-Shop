import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Globe, Users, Sparkles, Mail, Phone, MapPin } from 'lucide-react';

const About = () => {
  const navigate = useNavigate();
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-brand-pink py-20 px-6 text-center">
        <h1 className="text-5xl font-serif text-gray-900 mb-6">Redefining Beauty</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
          We believe beauty is not about covering up, but about revealing the true radiance that lies within you.
        </p>
      </section>

      {/* Our Story */}
      <section className="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-2 gap-12 items-center">
        <div className="relative aspect-[4/5] bg-gray-100 rounded-2xl overflow-hidden">
          <img 
            src="https://i.pinimg.com/736x/fc/5e/48/fc5e4818733b2e473bf92c4dfc78bced.jpg" 
            alt="Our Founder" 
            className="w-full h-full object-cover"
          />
        </div>
        <div className="space-y-6">
          <h2 className="text-3xl font-serif text-gray-900">Our Story</h2>
          <p className="text-gray-600 leading-relaxed">
            Founded in 2024, Bloom Beauty began with a simple question: Why must effective skincare be complicated? 
            Frustrated by 10-step routines and unpronounceable ingredients, we set out to create a line of products 
            that are as kind to the earth as they are to your skin.
          </p>
          <p className="text-gray-600 leading-relaxed">
            Every product we make is crafted with intention, using ethically sourced botanicals and clinical-grade 
            actives to deliver real results without the fluff. Our mission is to make premium beauty accessible 
            to everyone, regardless of budget or beauty expertise.
          </p>
          <p className="text-gray-600 leading-relaxed">
            From our humble beginnings in a small lab to serving thousands of customers worldwide, we remain 
            committed to transparency, sustainability, and most importantly, helping you feel confident in your own skin.
          </p>
        </div>
      </section>

      {/* Values */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-serif mb-4">Our Core Values</h2>
            <div className="w-24 h-1 bg-pink-600 mx-auto"></div>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { icon: Heart, title: "Cruelty Free", desc: "We never test on animals, ever. All our products are certified cruelty-free." },
              { icon: Globe, title: "Sustainable", desc: "Packaging made from recycled materials with carbon-neutral shipping." },
              { icon: Users, title: "Inclusive", desc: "Formulated for all skin types, tones, and ages. Beauty has no boundaries." },
              { icon: Sparkles, title: "Clean", desc: "No parabens, sulfates, or harmful toxins. Just pure, effective ingredients." },
            ].map((item, idx) => (
              <div key={idx} className="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition text-center">
                <div className="text-pink-600 flex justify-center mb-4"><item.icon size={32} /></div>
                <h3 className="font-bold text-lg mb-2">{item.title}</h3>
                <p className="text-sm text-gray-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-serif mb-4">Meet Our Team</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Behind every great product is a passionate team dedicated to bringing you the best in beauty innovation.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { name: "Natalie Keen", role: "Founder & CEO", image: "https://i.pinimg.com/736x/15/14/bb/1514bb7cd66f7494a8a4643696cf8ab0.jpg" },
            { name: "Dr. Maria James", role: "Head of R&D", image: "https://i.pinimg.com/736x/85/8d/77/858d777a89e67ab024cdbd1412a603aa.jpg" },
            { name: "James Wilson", role: "Sustainability Director", image: "https://i.pinimg.com/736x/64/18/fb/6418fbb386606f49f05a9692908ebd1a.jpg" },
          ].map((member, idx) => (
            <div key={idx} className="text-center">
              <div className="w-32 h-32 mx-auto mb-4 rounded-full overflow-hidden">
                <img src={member.image} alt={member.name} className="w-full h-full object-cover" />
              </div>
              <h3 className="font-bold text-lg text-gray-900">{member.name}</h3>
              <p className="text-pink-600 font-medium">{member.role}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Contact CTA */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-serif mb-4 text-gray-900">Ready to Start Your Beauty Journey?</h2>
          <p className="text-xl mb-8 text-gray-600">
            Have questions about our products or want to learn more about our mission? We'd love to hear from you.
          </p>
          <button
            onClick={() => navigate('/contact')}
            className="inline-flex items-center gap-2 bg-gray-900 text-white px-8 py-4 rounded-full font-bold hover:bg-gray-800 transition-colors"
          >
            <Mail size={20} />
            Contact Us
          </button>
        </div>
      </section>
    </div>
  );
};

export default About;
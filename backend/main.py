from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import json
import os
from datetime import datetime

app = FastAPI(
    title="Aryan Thakur Portfolio API",
    description="Backend API for Aryan Thakur's professional portfolio",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class Project(BaseModel):
    id: str
    title: str
    description: str
    technologies: List[str]
    category: str
    image_url: str
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    featured: bool = False

class BlogPost(BaseModel):
    id: str
    title: str
    excerpt: str
    content: str
    published_date: datetime
    tags: List[str]
    featured: bool = False

class Testimonial(BaseModel):
    id: str
    name: str
    role: str
    company: str
    content: str
    avatar_url: str
    rating: int

# Sample data
PROJECTS = [
    Project(
        id="universal-cloud",
        title="Universal Cloud — Client & Admin Suite",
        description="Complete hosting platform with client management, invoicing, developer assignment, and Discord integration.",
        technologies=["Next.js", "Node.js", "Firebase", "Cloudflare", "TypeScript"],
        category="Web",
        image_url="/images/projects/universal-cloud.jpg",
        live_url="https://universal-cloud.com",
        github_url="https://github.com/aryan/universal-cloud",
        featured=True
    ),
    Project(
        id="black-aviator",
        title="Black Aviator — Real-Time Game",
        description="Crash-style betting game with admin-only bet visibility, Razorpay integration, and wallet system.",
        technologies=["Kotlin", "Android", "WebSockets", "Razorpay", "Firebase"],
        category="Games",
        image_url="/images/projects/black-aviator.jpg",
        live_url="https://play.google.com/store/apps/details?id=com.blackaviator",
        featured=True
    ),
    Project(
        id="ai-ops-tools",
        title="AI Ops Tools",
        description="Role-based AI assistants with analytics, data pipelines, and automation workflows.",
        technologies=["Next.js", "OpenAI API", "Vector DB", "Python", "FastAPI"],
        category="AI",
        image_url="/images/projects/ai-ops.jpg",
        github_url="https://github.com/aryan/ai-ops-tools",
        featured=True
    ),
    Project(
        id="discord-telegram-bots",
        title="Discord/Telegram Bots Suite",
        description="Music bots, moderation tools, queue management, Spotify API integration, and Firebase queues.",
        technologies=["Node.js", "discord.js", "Telegram Bot API", "Firebase", "Spotify API"],
        category="Bots",
        image_url="/images/projects/bots-suite.jpg",
        github_url="https://github.com/aryan/discord-telegram-bots",
        featured=True
    )
]

BLOG_POSTS = [
    BlogPost(
        id="building-scalable-web-apps",
        title="Building Scalable Web Applications with React and TypeScript",
        excerpt="Learn how to create production-ready web applications that scale with your business needs.",
        content="Full blog content here...",
        published_date=datetime(2025, 1, 15),
        tags=["React", "TypeScript", "Web Development", "Scalability"],
        featured=True
    ),
    BlogPost(
        id="ai-integration-best-practices",
        title="AI Integration Best Practices for Modern Web Apps",
        excerpt="Discover how to effectively integrate AI capabilities into your web applications.",
        content="Full blog content here...",
        published_date=datetime(2025, 1, 10),
        tags=["AI", "Machine Learning", "Web Development", "Best Practices"],
        featured=True
    )
]

TESTIMONIALS = [
    Testimonial(
        id="client-1",
        name="Sarah Johnson",
        role="Product Manager",
        company="TechCorp",
        content="Aryan delivered an exceptional web application that exceeded our expectations. His attention to detail and technical expertise is outstanding.",
        avatar_url="/images/testimonials/sarah.jpg",
        rating=5
    ),
    Testimonial(
        id="client-2",
        name="Michael Chen",
        role="CEO",
        company="StartupXYZ",
        content="Working with Aryan was a game-changer for our business. He built us a robust Discord bot that automated our entire customer support workflow.",
        avatar_url="/images/testimonials/michael.jpg",
        rating=5
    )
]

# API Routes
@app.get("/")
async def root():
    return {"message": "Aryan Thakur Portfolio API", "version": "1.0.0"}

@app.get("/api/projects", response_model=List[Project])
async def get_projects(category: Optional[str] = None, featured: Optional[bool] = None):
    """Get all projects, optionally filtered by category or featured status"""
    projects = PROJECTS
    
    if category:
        projects = [p for p in projects if p.category.lower() == category.lower()]
    
    if featured is not None:
        projects = [p for p in projects if p.featured == featured]
    
    return projects

@app.get("/api/projects/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    project = next((p for p in PROJECTS if p.id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.get("/api/blog", response_model=List[BlogPost])
async def get_blog_posts(featured: Optional[bool] = None, limit: Optional[int] = None):
    """Get all blog posts, optionally filtered by featured status"""
    posts = BLOG_POSTS
    
    if featured is not None:
        posts = [p for p in posts if p.featured == featured]
    
    # Sort by published date (newest first)
    posts = sorted(posts, key=lambda x: x.published_date, reverse=True)
    
    if limit:
        posts = posts[:limit]
    
    return posts

@app.get("/api/blog/{post_id}", response_model=BlogPost)
async def get_blog_post(post_id: str):
    """Get a specific blog post by ID"""
    post = next((p for p in BLOG_POSTS if p.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post

@app.get("/api/testimonials", response_model=List[Testimonial])
async def get_testimonials():
    """Get all testimonials"""
    return TESTIMONIALS

@app.post("/api/contact")
async def submit_contact_form(contact: ContactForm):
    """Submit contact form"""
    # In a real application, you would:
    # 1. Validate the input
    # 2. Save to database
    # 3. Send email notification
    # 4. Return appropriate response
    
    # For now, just log the contact form data
    print(f"Contact form submitted: {contact.dict()}")
    
    return {
        "message": "Thank you for your message! I'll get back to you soon.",
        "status": "success"
    }

@app.get("/api/skills")
async def get_skills():
    """Get skills and technologies"""
    skills = {
        "Frontend": [
            {"name": "React", "level": 95, "icon": "react"},
            {"name": "TypeScript", "level": 90, "icon": "typescript"},
            {"name": "JavaScript", "level": 95, "icon": "javascript"},
            {"name": "Tailwind CSS", "level": 90, "icon": "tailwind"},
            {"name": "Three.js", "level": 80, "icon": "threejs"}
        ],
        "Backend": [
            {"name": "Node.js", "level": 90, "icon": "nodejs"},
            {"name": "Python", "level": 85, "icon": "python"},
            {"name": "FastAPI", "level": 80, "icon": "fastapi"},
            {"name": "Firebase", "level": 85, "icon": "firebase"}
        ],
        "Mobile": [
            {"name": "Kotlin", "level": 80, "icon": "kotlin"},
            {"name": "Android Studio", "level": 75, "icon": "android"}
        ],
        "Tools & Others": [
            {"name": "Git", "level": 90, "icon": "git"},
            {"name": "Docker", "level": 75, "icon": "docker"},
            {"name": "Cloudflare", "level": 80, "icon": "cloudflare"},
            {"name": "Razorpay", "level": 85, "icon": "razorpay"}
        ]
    }
    return skills

@app.get("/api/services")
async def get_services():
    """Get services offered"""
    services = [
        {
            "id": "web-development",
            "title": "Web Apps & Dashboards",
            "description": "Next.js/React applications with role-based access, admin consoles, analytics, and SEO optimization.",
            "icon": "code",
            "features": ["Responsive Design", "SEO Optimized", "Admin Dashboards", "Real-time Analytics"]
        },
        {
            "id": "ai-automation",
            "title": "AI Tools & Automation",
            "description": "OpenAI integrations, RAG systems, vector search, and task automation workflows.",
            "icon": "brain",
            "features": ["OpenAI Integration", "Vector Search", "RAG Systems", "Workflow Automation"]
        },
        {
            "id": "bot-development",
            "title": "Discord/Telegram Bots",
            "description": "Music bots, moderation tools, payment integration, CRM hooks, and Firebase queues.",
            "icon": "bot",
            "features": ["Music & VC", "Moderation", "Payment Integration", "Custom Commands"]
        },
        {
            "id": "game-development",
            "title": "Game Systems",
            "description": "Real-time game mechanics, wallet systems, anti-cheat, admin insights, and payment integration.",
            "icon": "gamepad",
            "features": ["Real-time Logic", "Payment Systems", "Admin Controls", "Anti-cheat"]
        }
    ]
    return services

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
